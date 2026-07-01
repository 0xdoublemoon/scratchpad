#!/usr/bin/env python3
"""
extract_epub.py — Mechanical EPUB -> text extractor for the book-to-skill pipeline.

Does the DETERMINISTIC part of the job only: unzip the EPUB, read its reading
order (spine) and table of contents (nav/ncx), strip each content document to
clean text, estimate token counts, and write everything to an output directory.
The DISTILLATION (thesis, frameworks, anti-patterns) is NOT done here — that is
the LLM's job, guided by SKILL.md.

Stdlib only. Works on EPUB 2 (toc.ncx) and EPUB 3 (nav.xhtml).

Usage:
    python extract_epub.py <book.epub> <output_dir>

Outputs:
    <output_dir>/book.json          metadata + ordered chapter list w/ token estimates
    <output_dir>/chapters/NN-slug.txt   clean text per spine document
    <output_dir>/full_text.txt      whole book concatenated (for global reads)
"""

import sys
import os
import re
import json
import zipfile
import posixpath
from html.parser import HTMLParser
from xml.etree import ElementTree as ET


# ---------- helpers ----------

def strip_ns(tag):
    """Drop the {namespace} prefix ElementTree prepends, so we can match tags simply."""
    return tag.split('}')[-1] if '}' in tag else tag


def est_tokens(text):
    """Rough token estimate, CJK-aware.

    Latin prose is ~4 chars/token, but CJK characters are ~1 token each, so a
    flat chars/4 badly under-counts Chinese/Japanese/Korean text. Count CJK
    codepoints at ~1 token and everything else at 4 chars/token. Conservative
    (leans high) on purpose, so generated skills stay within real budgets.
    """
    cjk = sum(
        1 for ch in text
        if '\u4e00' <= ch <= '\u9fff'     # CJK unified ideographs
        or '\u3040' <= ch <= '\u30ff'     # hiragana + katakana
        or '\uac00' <= ch <= '\ud7a3'     # hangul syllables
        or '\uf900' <= ch <= '\ufaff'     # CJK compatibility ideographs
    )
    other = len(text) - cjk
    return max(1, round(cjk + other / 4))


def slugify(text, maxlen=40):
    text = re.sub(r'[^\w\s-]', '', text or '').strip().lower()
    text = re.sub(r'[\s_-]+', '-', text)
    return (text[:maxlen].rstrip('-')) or 'section'


BLOCK_TAGS = {
    'p', 'div', 'br', 'li', 'tr', 'section', 'article', 'header', 'footer',
    'blockquote', 'figure', 'figcaption', 'pre', 'ul', 'ol', 'table', 'hr',
}
HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
SKIP_TAGS = {'script', 'style', 'head', 'nav'}


class TextExtractor(HTMLParser):
    """Turn XHTML into readable plain text, keeping headings as markdown-ish markers."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip_depth = 0
        self._heading = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        elif tag in HEADING_TAGS:
            level = int(tag[1])
            self.parts.append('\n\n' + '#' * level + ' ')
            self._heading = tag
        elif tag in BLOCK_TAGS:
            self.parts.append('\n\n')

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in HEADING_TAGS:
            self.parts.append('\n')
            self._heading = None
        elif tag in BLOCK_TAGS:
            self.parts.append('\n')

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.parts.append(data)

    def get_text(self):
        text = ''.join(self.parts)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' *\n *', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def html_to_text(raw_bytes):
    try:
        html = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        html = raw_bytes.decode('utf-8', errors='replace')
    p = TextExtractor()
    try:
        p.feed(html)
    except Exception:
        # Fall back to a crude tag strip if the parser chokes on malformed markup.
        return re.sub(r'<[^>]+>', ' ', html)
    return p.get_text()


# ---------- EPUB structure parsing ----------

def find_opf_path(z):
    data = z.read('META-INF/container.xml')
    root = ET.fromstring(data)
    for el in root.iter():
        if strip_ns(el.tag) == 'rootfile':
            return el.attrib.get('full-path')
    raise RuntimeError('Could not locate OPF via container.xml')


def parse_opf(z, opf_path):
    root = ET.fromstring(z.read(opf_path))
    opf_dir = posixpath.dirname(opf_path)

    meta = {'title': None, 'author': None}
    manifest = {}   # id -> {'href':..., 'media_type':..., 'props':...}
    spine = []      # ordered idrefs
    ncx_id = None

    for el in root.iter():
        tag = strip_ns(el.tag)
        if tag == 'title' and meta['title'] is None:
            meta['title'] = (el.text or '').strip() or None
        elif tag == 'creator' and meta['author'] is None:
            meta['author'] = (el.text or '').strip() or None
        elif tag == 'item':
            manifest[el.attrib.get('id')] = {
                'href': el.attrib.get('href'),
                'media_type': el.attrib.get('media-type', ''),
                'props': el.attrib.get('properties', ''),
            }
        elif tag == 'itemref':
            if el.attrib.get('linear', 'yes') != 'no':
                spine.append(el.attrib.get('idref'))
        elif tag == 'spine':
            ncx_id = el.attrib.get('toc')

    def resolve(href):
        return posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href

    # Resolve spine idrefs to actual content file paths (documents only).
    spine_files = []
    for idref in spine:
        item = manifest.get(idref)
        if item and 'html' in item['media_type']:
            spine_files.append(resolve(item['href']))

    # Locate the nav document (EPUB3) or the ncx (EPUB2) for chapter titles.
    nav_path = None
    for item in manifest.values():
        if 'nav' in (item.get('props') or ''):
            nav_path = resolve(item['href'])
            break
    ncx_path = None
    if ncx_id and ncx_id in manifest:
        ncx_path = resolve(manifest[ncx_id]['href'])
    else:
        for item in manifest.values():
            if item['media_type'] == 'application/x-dtbncx+xml':
                ncx_path = resolve(item['href'])
                break

    return meta, spine_files, nav_path, ncx_path


def parse_titles(z, nav_path, ncx_path):
    """Return {content_file_path (no #fragment) -> title}. Best-effort."""
    titles = {}

    def norm(target, base):
        target = target.split('#')[0]
        if not target:
            return None
        base_dir = posixpath.dirname(base)
        return posixpath.normpath(posixpath.join(base_dir, target)) if base_dir else target

    # EPUB3 nav.xhtml: <a href="chapter.xhtml">Title</a>
    if nav_path:
        try:
            root = ET.fromstring(z.read(nav_path))
            for a in root.iter():
                if strip_ns(a.tag) == 'a':
                    href = a.attrib.get('href')
                    text = ''.join(a.itertext()).strip()
                    key = norm(href, nav_path) if href else None
                    if key and text and key not in titles:
                        titles[key] = text
        except Exception:
            pass

    # EPUB2 toc.ncx: <navPoint><navLabel><text>Title</text><content src="..."/>
    if ncx_path and not titles:
        try:
            root = ET.fromstring(z.read(ncx_path))
            for np in root.iter():
                if strip_ns(np.tag) != 'navPoint':
                    continue
                label, src = None, None
                for child in np.iter():
                    t = strip_ns(child.tag)
                    if t == 'text' and label is None:
                        label = (child.text or '').strip()
                    elif t == 'content':
                        src = child.attrib.get('src')
                key = norm(src, ncx_path) if src else None
                if key and label and key not in titles:
                    titles[key] = label
        except Exception:
            pass

    return titles


# ---------- main ----------

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    epub_path, out_dir = sys.argv[1], sys.argv[2]
    if not os.path.isfile(epub_path):
        print(f"ERROR: not a file: {epub_path}")
        sys.exit(1)

    chapters_dir = os.path.join(out_dir, 'chapters')
    os.makedirs(chapters_dir, exist_ok=True)

    with zipfile.ZipFile(epub_path) as z:
        opf_path = find_opf_path(z)
        meta, spine_files, nav_path, ncx_path = parse_opf(z, opf_path)
        titles = parse_titles(z, nav_path, ncx_path)

        chapters = []
        full_parts = []
        idx = 0
        for path in spine_files:
            try:
                raw = z.read(path)
            except KeyError:
                continue
            text = html_to_text(raw)
            if len(text) < 200:   # skip covers, blank pages, tiny nav stubs
                continue
            idx += 1

            title = titles.get(path)
            if not title:
                m = re.search(r'^#+\s*(.+)$', text, re.MULTILINE)
                title = m.group(1).strip() if m else f'Section {idx}'
            title = re.sub(r'\s+', ' ', title)[:120]

            slug = slugify(title)
            fname = f'{idx:02d}-{slug}.txt'
            with open(os.path.join(chapters_dir, fname), 'w', encoding='utf-8') as f:
                f.write(f'# {title}\n\n{text}\n')

            tokens = est_tokens(text)
            chapters.append({
                'index': idx,
                'title': title,
                'source_file': path,
                'text_file': f'chapters/{fname}',
                'chars': len(text),
                'est_tokens': tokens,
            })
            full_parts.append(f'\n\n===== [{idx:02d}] {title} =====\n\n{text}')

    with open(os.path.join(out_dir, 'full_text.txt'), 'w', encoding='utf-8') as f:
        f.write(''.join(full_parts).strip() + '\n')

    book = {
        'title': meta['title'] or os.path.splitext(os.path.basename(epub_path))[0],
        'author': meta['author'],
        'source_epub': os.path.basename(epub_path),
        'chapter_count': len(chapters),
        'total_est_tokens': sum(c['est_tokens'] for c in chapters),
        'chapters': chapters,
    }
    with open(os.path.join(out_dir, 'book.json'), 'w', encoding='utf-8') as f:
        json.dump(book, f, indent=2, ensure_ascii=False)

    # Console summary for the operator.
    print(f"Title : {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Chapters extracted: {book['chapter_count']}")
    print(f"Total est. tokens : {book['total_est_tokens']:,}")
    print(f"Output dir: {out_dir}")
    print("\n#   tokens  title")
    print("-" * 60)
    for c in chapters:
        print(f"{c['index']:>2}  {c['est_tokens']:>6}  {c['title'][:48]}")


if __name__ == '__main__':
    main()

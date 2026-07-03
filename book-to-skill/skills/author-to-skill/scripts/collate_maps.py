#!/usr/bin/env python3
"""
collate_maps.py — Assemble every per-book concept map into ONE synthesis input.

The author layer is synthesized from the compressed per-book *maps*, not from the
full text of every book (which would never fit in context). This script gathers
those maps, sorts the books chronologically, and writes a single document the
model then reads to do cross-book synthesis.

Expected layout (produced by running book-to-skill per book):

    <books_dir>/
      <book-slug>/
        map.md            # the book's Tier-1 concept map (book-to-skill's SKILL.md body)
        meta.json         # optional: {"title": "...", "year": 2019}
        chapters/*.md     # Tier-2 toolkits (not read here)

If meta.json is absent, the script falls back to book.json (from the extractor)
for the title, and marks the year unknown. Missing years weaken the evolution
timeline — the script warns when any are missing.

Usage:
    python collate_maps.py <books_dir> <output_file.md>
"""

import sys
import os
import re
import json
import glob

MAP_CANDIDATES = ['map.md', 'SKILL-map.md', 'SKILL.md', 'concept-map.md']


def strip_frontmatter(md):
    m = re.match(r'^---\n.*?\n---\n', md, re.DOTALL)
    return md[m.end():].lstrip() if m else md


def find_map(book_dir):
    for name in MAP_CANDIDATES:
        p = os.path.join(book_dir, name)
        if os.path.isfile(p):
            return p
    # fall back to any *map*.md
    hits = glob.glob(os.path.join(book_dir, '*map*.md'))
    return hits[0] if hits else None


def read_meta(book_dir, slug):
    title, year = None, None
    mp = os.path.join(book_dir, 'meta.json')
    if os.path.isfile(mp):
        try:
            d = json.load(open(mp, encoding='utf-8'))
            title = d.get('title')
            year = d.get('year')
        except Exception:
            pass
    if title is None:
        bp = os.path.join(book_dir, 'book.json')
        if os.path.isfile(bp):
            try:
                d = json.load(open(bp, encoding='utf-8'))
                title = d.get('title')
                year = year or d.get('year')
            except Exception:
                pass
    return (title or slug), year


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    books_dir, out_file = sys.argv[1], sys.argv[2]
    if not os.path.isdir(books_dir):
        print(f"ERROR: not a directory: {books_dir}")
        sys.exit(1)

    books = []
    for entry in sorted(os.listdir(books_dir)):
        book_dir = os.path.join(books_dir, entry)
        if not os.path.isdir(book_dir):
            continue
        map_path = find_map(book_dir)
        if not map_path:
            print(f"  warn: no map found in {entry}/ — skipping")
            continue
        title, year = read_meta(book_dir, entry)
        books.append({'slug': entry, 'title': title, 'year': year, 'map': map_path})

    if not books:
        print("ERROR: no per-book maps found. Run book-to-skill on each EPUB first.")
        sys.exit(1)

    # Chronological sort; unknown years sink to the end.
    books.sort(key=lambda b: (b['year'] is None, b['year'] or 0))
    missing_years = [b['title'] for b in books if b['year'] is None]

    lines = []
    lines.append("# Author synthesis input\n")
    lines.append(f"{len(books)} books, chronological. Synthesize the AUTHOR layer "
                 "from the maps below — cluster recurring frameworks semantically, "
                 "trace evolution across years, name the through-lines and method.\n")
    lines.append("## Book table (chronological)\n")
    lines.append("| # | year | title | slug |")
    lines.append("|---|------|-------|------|")
    for i, b in enumerate(books, 1):
        lines.append(f"| {i} | {b['year'] or '????'} | {b['title']} | {b['slug']} |")
    lines.append("")

    for i, b in enumerate(books, 1):
        body = strip_frontmatter(open(b['map'], encoding='utf-8').read()).strip()
        lines.append(f"\n\n===== BOOK {i} · {b['title']} ({b['year'] or 'year unknown'}) · "
                     f"slug={b['slug']} =====\n")
        lines.append(body)

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Collated {len(books)} book maps → {out_file}")
    for b in books:
        print(f"  [{b['year'] or '????'}] {b['title']}  ({b['slug']})")
    if missing_years:
        print(f"\n  ⚠ {len(missing_years)} book(s) missing a year: "
              f"{', '.join(missing_years)}")
        print("    → Ask the user for publication years, or weaken the evolution "
              "timeline section (don't fabricate an order).")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
check_author_budget.py — Validate a generated AUTHOR skill against token budgets.

Three tiers:
  Tier 0  SKILL.md body (author concept map)          target ~3,500 (hard 4,200)
  Tier 1  references/books/<slug>/map.md (per book)   target ~1,500 (hard 1,800)
  Tier 2  references/books/<slug>/chapters/*.md        target ~1,000 (hard 1,200)

Token counts are CJK-aware (CJK codepoints ~1 token, other text ~4 chars/token).
Over-hard-ceiling files are flagged and set a non-zero exit code.

Usage:
    python check_author_budget.py <author_skill_dir>
"""

import sys
import os
import re
import glob

T0_TARGET, T0_HARD = 3500, 4200
T1_TARGET, T1_HARD = 1500, 1800
T2_TARGET, T2_HARD = 1000, 1200

MAP_CANDIDATES = ['map.md', 'SKILL-map.md', 'concept-map.md']


def est_tokens(text):
    cjk = sum(
        1 for ch in text
        if '\u4e00' <= ch <= '\u9fff'
        or '\u3040' <= ch <= '\u30ff'
        or '\uac00' <= ch <= '\ud7a3'
        or '\uf900' <= ch <= '\ufaff'
    )
    return max(1, round(cjk + (len(text) - cjk) / 4))


def strip_frontmatter(md):
    m = re.match(r'^---\n.*?\n---\n', md, re.DOTALL)
    return md[m.end():] if m else md


def flag(tok, target, hard):
    if tok <= target:
        return ''
    return '  ~over target' if tok <= hard else '  !! OVER BUDGET'


def find_map(book_dir):
    for name in MAP_CANDIDATES:
        p = os.path.join(book_dir, name)
        if os.path.isfile(p):
            return p
    hits = glob.glob(os.path.join(book_dir, '*map*.md'))
    return hits[0] if hits else None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    root = sys.argv[1]
    skill_md = os.path.join(root, 'SKILL.md')
    if not os.path.isfile(skill_md):
        print(f"ERROR: no SKILL.md in {root}")
        sys.exit(1)

    ok = True

    body = strip_frontmatter(open(skill_md, encoding='utf-8').read())
    t0 = est_tokens(body)
    f0 = flag(t0, T0_TARGET, T0_HARD)
    ok = ok and t0 <= T0_HARD
    print(f"[Tier 0] SKILL.md (author map)          {t0:>5} tok  (target {T0_TARGET}){f0}")

    books_dir = os.path.join(root, 'references', 'books')
    if not os.path.isdir(books_dir):
        print("\n(no references/books/ directory found)")
        print("\nRESULT:", "within budget ✅" if ok else "over budget ❌")
        sys.exit(0 if ok else 2)

    for slug in sorted(os.listdir(books_dir)):
        book_dir = os.path.join(books_dir, slug)
        if not os.path.isdir(book_dir):
            continue
        print(f"\n  book: {slug}")
        mp = find_map(book_dir)
        if mp:
            t1 = est_tokens(open(mp, encoding='utf-8').read())
            f1 = flag(t1, T1_TARGET, T1_HARD)
            ok = ok and t1 <= T1_HARD
            print(f"  [Tier 1] {os.path.basename(mp):<26} {t1:>5} tok  (target {T1_TARGET}){f1}")
        else:
            print("  [Tier 1] (no map.md found)")
        for ch in sorted(glob.glob(os.path.join(book_dir, 'chapters', '*.md'))):
            t2 = est_tokens(open(ch, encoding='utf-8').read())
            f2 = flag(t2, T2_TARGET, T2_HARD)
            ok = ok and t2 <= T2_HARD
            print(f"  [Tier 2] {os.path.basename(ch):<26} {t2:>5} tok  (target {T2_TARGET}){f2}")

    print()
    print("RESULT:", "within budget ✅" if ok else "over budget — compress flagged files ❌")
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()

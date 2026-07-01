#!/usr/bin/env python3
"""
check_budget.py — Validate a generated two-tier skill against its token budgets.

Tier 1 (SKILL.md body, the always-loaded concept map): target ~3,000 tokens.
Tier 2 (each references/*.md chapter toolkit):          target ~1,000 tokens.

Token counts are estimated at ~4 chars/token (frontmatter excluded from the
Tier-1 count, since it is metadata, not body). Over-budget files are flagged so
you can compress before shipping.

Usage:
    python check_budget.py <generated_skill_dir>
"""

import sys
import os
import re
import glob

TIER1_TARGET = 3000
TIER1_HARD = 3600      # 20% headroom before it's a real problem
TIER2_TARGET = 1000
TIER2_HARD = 1200


def est_tokens(text):
    """CJK-aware: CJK codepoints ~1 token each, other text ~4 chars/token."""
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


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    skill_dir = sys.argv[1]
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.isfile(skill_md):
        print(f"ERROR: no SKILL.md in {skill_dir}")
        sys.exit(1)

    ok = True

    with open(skill_md, encoding='utf-8') as f:
        body = strip_frontmatter(f.read())
    t1 = est_tokens(body)
    flag = '' if t1 <= TIER1_TARGET else ('  ~over target' if t1 <= TIER1_HARD else '  !! OVER BUDGET')
    if t1 > TIER1_HARD:
        ok = False
    print(f"[Tier 1] SKILL.md body          {t1:>5} tok  (target {TIER1_TARGET}){flag}")

    print()
    refs = sorted(glob.glob(os.path.join(skill_dir, 'references', '*.md')))
    if not refs:
        print("[Tier 2] no references/*.md found")
    for path in refs:
        with open(path, encoding='utf-8') as f:
            t2 = est_tokens(f.read())
        name = os.path.basename(path)
        flag = '' if t2 <= TIER2_TARGET else ('  ~over target' if t2 <= TIER2_HARD else '  !! OVER BUDGET')
        if t2 > TIER2_HARD:
            ok = False
        print(f"[Tier 2] {name:<28} {t2:>5} tok  (target {TIER2_TARGET}){flag}")

    print()
    print("RESULT:", "within budget ✅" if ok else "over budget — compress flagged files ❌")
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()

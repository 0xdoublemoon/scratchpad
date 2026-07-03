# book-to-skill (Claude Code plugin)

Turn a non-fiction EPUB into a two-tier Claude Code skill:

- **Tier 1 — concept map** (always loaded, ~3K tokens): thesis, 6–10 load-bearing
  frameworks, a chapter index, and a topic index.
- **Tier 2 — chapter toolkits** (on-demand, ~1K tokens each): frameworks,
  techniques, anti-patterns, and worked examples per chapter.

The output structure mirrors Claude Code's own progressive disclosure: the concept
map becomes the generated skill's `SKILL.md`, and each chapter toolkit becomes a
`references/*.md` file loaded only when needed.

## Structure

```
book-to-skill/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest
│   └── marketplace.json     # self-referencing local marketplace (for one-command install)
├── skills/
│   ├── book-to-skill/       # the meta-skill: EPUB → two-tier skill
│   │   ├── SKILL.md         # workflow + distillation principles + copyright rules
│   │   ├── scripts/
│   │   │   ├── extract_epub.py   # EPUB → book.json + per-chapter text + CJK-aware token counts
│   │   │   └── check_budget.py   # validates the generated skill against token budgets
│   │   └── references/
│   │       ├── tier1-concept-map-template.md
│   │       └── tier2-chapter-toolkit-template.md
│   ├── author-to-skill/    # the meta-skill: an author's whole corpus → three-tier skill
│   │   ├── SKILL.md         # workflow + semantic-clustering + reconciliation rules
│   │   ├── scripts/
│   │   │   ├── collate_maps.py        # merges per-book maps into one synthesis input
│   │   │   └── check_author_budget.py # validates the three-tier tree against token budgets
│   │   └── references/
│   │       ├── synthesis-guide.md
│   │       └── tier0-author-map-template.md
│   └── second-brain/        # example OUTPUT skill, generated from *Building a Second Brain*
│       ├── SKILL.md         # Tier-1 concept map (CODE + PARA)
│       └── references/       # 9 Tier-2 chapter toolkits (ch02–ch10)
└── README.md
```

This plugin bundles three skills: `book-to-skill` (the generator, one book →
two tiers), `author-to-skill` (the generator, one author's books → three tiers,
built on top of `book-to-skill`), and `second-brain` (a worked example of what
the generator produces — the concept map + chapter toolkits distilled from
Tiago Forte's *Building a Second Brain*).

## Install (local, no GitHub needed)

Drop this `book-to-skill/` folder into `~/Projects/scratchpad/`, then inside
Claude Code:

```
/plugin marketplace add ~/Projects/scratchpad/book-to-skill
/plugin install book-to-skill@book-to-skill-dev
```

Restart the session if prompted. Verify the skills are available:

```
/plugin list
```

Installing the plugin makes all three skills available: `book-to-skill` (the
generator), `author-to-skill` (the multi-book generator), and `second-brain`
(the example output skill).

## Use

Give Claude Code an EPUB and ask it to make a skill, e.g.:

> 把这本书做成 skill: ./books/atomic-habits.epub

Claude will extract the EPUB, distill the concept map and chapter toolkits, check
the token budgets, and assemble a new skill folder you can install the same way.

To distill several books by the same author into one skill, e.g.:

> 把某作者的书都做成 skill: ./books/author-x/*.epub

Claude will run `book-to-skill` once per book, collate the resulting concept maps,
synthesize the cross-book author layer (frameworks, through-lines, evolution
timeline, method & voice), and assemble a three-tier skill folder.

## Notes

- Scripts are pure Python stdlib — no `pip install` required. Works on EPUB 2
  (`toc.ncx`) and EPUB 3 (`nav.xhtml`).
- Token estimates are CJK-aware (CJK codepoints ≈ 1 token; other text ≈ 4 chars/token).
- The skill enforces copyright limits: it distills and paraphrases, and never
  reproduces long verbatim passages from the book.
- Scope is **non-fiction** (how-to / business / technical / methodology). Fiction
  and narrative memoir don't fit the framework/technique/anti-pattern shape.

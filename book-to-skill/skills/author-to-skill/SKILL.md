---
name: author-to-skill
description: >
  Distill an author's whole body of work into a three-tier Claude Code skill: an
  always-loaded author concept map (cross-book frameworks, through-lines, evolution
  timeline, method & voice, bibliography) over per-book maps and per-chapter
  toolkits. Use this skill whenever the user wants to turn several books by one
  author into a single skill, synthesize an author's thinking across their works,
  build an "everything by X" knowledge base, or compare/trace ideas across an
  author's books. Triggers include: "把某作者的书都做成 skill", "蒸馏这个作者",
  "author to skill", "synthesize an author's books", "把这几本书合成一个作者 skill",
  "cross-book synthesis", "一个作者的知识体系". Builds on the book-to-skill skill,
  which it runs once per book.
---

# Author → Skill

Turn several books by one author into a **three-tier** skill:

- **Tier 0 — author map** (always loaded, ~3.5K): cross-book canonical frameworks,
  through-lines, evolution timeline, method & voice, bibliography graph.
- **Tier 1 — per-book maps** (on-demand, ~1.5K each): each book's concept map.
- **Tier 2 — chapter toolkits** (on-demand, ~1K each): frameworks / techniques /
  anti-patterns / worked examples per chapter.

**Why three tiers, not one big summary.** An author's full corpus (say 5 × ~100K
tokens) never fits in context, so you cannot "read everything then synthesize."
Progressive disclosure is not just a runtime loading trick here — it is the
compression that makes author-level synthesis *computationally* possible: each book
is first squeezed to a ~1.5K map, and the author layer is synthesized **only from
those maps**.

**Depends on `book-to-skill`.** This skill runs book-to-skill once per book for the
per-book layer, then adds the author layer on top. Keep both installed (they ship
together).

**Scope:** non-fiction, and a genuine single author across the books. Flag
co-authored or ghostwritten volumes — they dilute the author signal.

---

## Workflow

### Step 1 — Gather the corpus
Collect the author's EPUBs. For **each**, record the **publication year** (from the
user or the EPUB's `dc:date`); years drive the evolution timeline and their absence
weakens it. Confirm the books are genuinely by one author; note any co-authored or
ghostwritten ones and consider excluding them.

### Step 2 — Per-book distillation (delegate to book-to-skill)
For each EPUB, run the **book-to-skill** workflow to produce that book's concept map
and chapter toolkits. Write each book's output into:

```
references/books/<book-slug>/
├── map.md              # the book's concept map (book-to-skill's Tier-1 body, frontmatter stripped)
├── meta.json           # {"title": "...", "year": 2019}
└── chapters/
    ├── ch01-<slug>.md  # the book's Tier-2 toolkits
    └── ...
```

Nested book maps are loaded by pointer, not by trigger, so **strip the YAML
frontmatter** from each `map.md` — only the author-layer SKILL.md needs a
description. Write `meta.json` per book so the next steps can sort chronologically.

### Step 3 — Collate the maps
Concatenate every per-book map into one synthesis input (this is what makes the
author layer fit in context):

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/author-to-skill/scripts/collate_maps.py" \
    references/books  <work_dir>/author_synthesis_input.md
```

Read the warning about any missing years. If several are missing, ask the user or
plan to weaken the evolution section.

### Step 4 — Synthesize the author layer (the real work)
Read `references/synthesis-guide.md`, then read the collated
`author_synthesis_input.md` and produce the Tier-0 author map following
`references/tier0-author-map-template.md`. Working **only from the maps**, not the
full text:
- **Cluster frameworks semantically** across books → canonical name + gloss +
  per-book variants + depth pointer. A framework earns a Tier-0 slot only if it
  recurs across ≥2 books or is a clear career pillar.
- Name the **through-lines / worldview** (or honestly report eclecticism).
- Build the **evolution timeline** in publication order (needs years).
- Distill **method & voice** (how they argue — orthogonal to content, key to
  emulation).
- Write the **bibliography & reading map**.

The single hardest requirement: cluster by *function*, not wording. See the guide.

### Step 5 — Reconcile (second pass)
Revisit each `references/books/<slug>/map.md` and replace repeated explanations of a
shared framework with a back-reference to the canonical author-layer version, keeping
only that book's variant ("Framework X: see author map; this book adds Y"). This is
what stops five books from re-explaining the same model five times.

### Step 6 — Assemble & validate
Lay out the tree (Tier-0 `SKILL.md` + `references/books/<slug>/...`) and check budgets:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/author-to-skill/scripts/check_author_budget.py" <author-slug>/
```

Compress anything flagged over its ceiling, then re-run until it passes. Show the
user the author map and the budget table.

### Step 7 — Package
If the skill-creator packaging script is available, produce a `.skill` and present
it; otherwise present the folder for inspection and install.

---

## Synthesis principles

- **Semantic, not lexical.** Same-function ideas are one framework even with no shared
  words; same-word ideas with different substance are two. Reason about substance.
- **Canonical + variants**, never a re-listing of every book's frameworks.
- **Don't force coherence.** An eclectic author reported honestly beats a fake unified
  theory.
- **Evolution needs dates.** No reliable years → weaken or drop the timeline; never
  invent an order.
- **Current view + preserved arc.** When later books revise earlier ones, reflect the
  author's present position *and* record what changed and when.
- **Corpus is too big to read whole** — that's the point of the map layer. Synthesize
  from maps; only drill into a book's full text to resolve a specific ambiguity.
- **Copyright:** paraphrase and synthesize; never reproduce long verbatim passages.

## Reference files

- `references/synthesis-guide.md` — semantic clustering method + honest-handling
  pitfalls. Read before Step 4.
- `references/tier0-author-map-template.md` — exact structure + example for the author
  map. Read before Step 4.
- `scripts/collate_maps.py` — merge per-book maps into one synthesis input (Step 3).
- `scripts/check_author_budget.py` — validate the three-tier tree (Step 6).
- The per-book layers are produced by the **book-to-skill** skill (Step 2).

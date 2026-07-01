---
name: book-to-skill
description: >
  Convert a non-fiction EPUB into a two-tier Claude Code skill: an always-loaded
  concept map (~3K tokens — thesis, 6-10 load-bearing frameworks, chapter and
  topic indexes) plus on-demand chapter toolkits (~1K tokens each — frameworks,
  techniques, anti-patterns, worked examples). Use this skill whenever the user
  wants to turn a book into a skill, distill an EPUB into reusable knowledge,
  build a concept map from a book, or make a book's methods available to Claude.
  Triggers include: "把这本书做成 skill", "把 epub 转成 skill", "distill this book",
  "turn this ebook into a skill", "帮我把这本书蒸馏成框架", "make a skill from this
  book", "book to skill". Trigger even when the user just uploads an .epub and
  asks to "make this usable" or "extract the frameworks".
---

# Book → Skill

Turn a non-fiction EPUB into a reusable, progressively-disclosed skill.

The output mirrors how skills load: the **concept map** becomes the generated
skill's `SKILL.md` (always in context), and each **chapter toolkit** becomes a
`references/*.md` file (loaded only when needed). You are compressing a whole
book into ~3K always-on tokens plus a set of ~1K on-demand toolkits.

**Division of labor:** the bundled script does the mechanical extraction
(unzip, reading order, chapter titles, clean text, token counts). *You* do the
distillation — identifying the thesis, the load-bearing frameworks, the
anti-patterns. A script cannot judge what is load-bearing; that is the whole
value you add.

**Scope:** this is for **non-fiction** — how-to, business, technical, science,
self-improvement, methodology. The thesis/framework/technique/anti-pattern
shape does not fit fiction or narrative memoir; if handed one, say so and stop.

---

## Workflow

### Step 1 — Extract the EPUB

Run the extractor (stdlib only, no install needed). Inside a Claude Code plugin
its absolute path is `${CLAUDE_PLUGIN_ROOT}/skills/book-to-skill/scripts/extract_epub.py`;
as a standalone skill it is `scripts/extract_epub.py` relative to this skill folder.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/book-to-skill/scripts/extract_epub.py" <path/to/book.epub> <work_dir>
```

It writes `<work_dir>/book.json` (title, author, ordered chapter list with
per-chapter token estimates), `<work_dir>/chapters/NN-slug.txt` (clean text per
chapter), and `<work_dir>/full_text.txt`. Read the console summary to see the
chapter map and sizes at a glance.

If extraction returns very few chapters or odd titles, the EPUB's nav may be
weak — open `full_text.txt` and use the `===== [NN] title =====` separators to
understand the real structure before proceeding.

### Step 2 — Read and plan

Read `book.json` for the shape, then read the chapters. For a normal book, read
it all. For a very long book, read every chapter's opening and closing plus any
chapter the index suggests is central; you need real understanding, not skimming
— the quality of the distillation is bounded by how well you actually read.

Then decide the **toolkit mapping** before writing anything:
- Default to one toolkit per chapter.
- **Drop** front/back matter with no reusable content (preface, acknowledgments,
  index) — they get no toolkit.
- **Merge** thin adjacent chapters that share one idea.
- **Split** an overlong chapter that carries two distinct methods.
- Target ~1K tokens per toolkit; if a chapter can't compress near that without
  losing load-bearing content, splitting is the signal.

Write the mapping down (a short list: which source chapters → which toolkit
files) so Steps 3-4 are mechanical.

### Step 3 — Write Tier 1: the concept map

Read `references/tier1-concept-map-template.md` and follow it exactly. This
becomes the generated skill's `SKILL.md`. It must:
- state the **thesis** (the one load-bearing argument),
- name **6-10 load-bearing frameworks** (models the book reuses — not one-offs),
- give a **chapter index** that routes each topic to its toolkit,
- give a **topic index** mapping the book's signature terms → chapter numbers,
- carry a **description** with concrete triggers derived from the book's domain,
  in the languages the user works in, and pushy enough to actually fire.

Budget: **~3,000 tokens** of body. The map's #1 job is *routing* — if you can't
tell from it which toolkit answers a question, it has failed.

### Step 4 — Write Tier 2: the chapter toolkits

Read `references/tier2-chapter-toolkit-template.md` and follow it exactly. For
each toolkit in your mapping, write `references/NN-<slug>.md` with all four
sections: **frameworks, techniques, anti-patterns, worked examples**. Make them
*operational* — a reader should be able to act from them, not just recall them.

Budget: **~1,000 tokens each** (hard ceiling ~1,200). Compress hard: drop
anecdote and repetition, keep the reusable skeleton and the author's vocabulary.

### Step 5 — Assemble and validate

Lay the generated skill out as its own folder:

```
<book-slug>/
├── SKILL.md                  # the Tier-1 concept map
└── references/
    ├── 01-<slug>.md          # Tier-2 toolkits
    ├── 02-<slug>.md
    └── ...
```

Check the budgets:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/book-to-skill/scripts/check_budget.py" <book-slug>/
```

(Standalone: `python scripts/check_budget.py <book-slug>/`.)
Compress anything flagged over budget, then re-run until it passes. Show the
user the budget table and the generated concept map.

### Step 6 — Package (if a file-delivery tool is available)

If the skill-creator packaging script is present, produce a `.skill`:

```bash
python /path/to/skill-creator/scripts/package_skill.py <book-slug>/
```

Then present the resulting file. Otherwise, present the folder / SKILL.md
directly so the user can inspect and install it.

---

## Distillation principles

These are what separate a real distillation from a book report.

- **Load-bearing only.** A framework earns a place in Tier 1 if the book *reuses*
  it to think. If it appears once and never returns, it belongs in a toolkit, not
  the map — or nowhere.
- **Distill for use, not for recall.** The test of a toolkit is "could someone
  act on this?", not "does this summarize the chapter?". Favor the technique over
  the anecdote that motivated it.
- **Keep the author's vocabulary.** The topic index and triggers only work if
  they match how the book — and its readers — name things. Don't rewrite the
  book's terms into generic ones.
- **Anti-patterns are gold.** Books encode hard-won "don't do this." Hunt for
  them explicitly; they're often buried in caveats and asides, and they're the
  most reusable part of a toolkit.
- **Compression is the craft.** Hitting ~3K + ~1K forces prioritization. When
  over budget, cut examples to one, cut adjectives, cut throat-clearing — never
  cut a load-bearing framework.

## Copyright — read this

A book-distillation tool must not become a reproduction tool. **Never** paste
long verbatim passages from the book into the generated skill. Frameworks,
techniques, and anti-patterns are stated in compressed, paraphrased form. Worked
examples are your own condensed retellings of the book's illustrations, not
copies of them. Short quoted phrases (well under a sentence) for a signature term
are fine; reproducing paragraphs, or so many small excerpts that the toolkit
substitutes for the book, is not. If the user asks for verbatim chapter text,
decline and offer the distilled toolkit instead.

## Reference files

- `references/tier1-concept-map-template.md` — exact structure + example for the
  always-loaded concept map (the generated `SKILL.md`). Read before Step 3.
- `references/tier2-chapter-toolkit-template.md` — exact structure + example for
  an on-demand chapter toolkit. Read before Step 4.
- `scripts/extract_epub.py` — mechanical EPUB → text/JSON extractor (Step 1).
- `scripts/check_budget.py` — token-budget validator for the output (Step 5).

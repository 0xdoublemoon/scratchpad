# Tier 0 — Author Concept Map Template (the author skill's SKILL.md)

The **always-loaded** author layer. It must let Claude (a) speak to the author's
whole body of work and route to the right book, and (b) reuse the author's shared
frameworks without loading every book. Budget: **~3,500 tokens** body (hard 4,200).

Copy this structure exactly.

---

```markdown
---
name: author-<slug>          # e.g. "author-tiago-forte"
description: >
  <Author>'s working knowledge, synthesized across <N> books (<year>–<year>). Use
  this skill whenever the user works in <the author's domain>, asks about <the
  author> or any of their books/frameworks, or wants to <apply / think with> their
  ideas. Triggers include: <author name>, <signature framework names>, <book
  titles>, <domain phrases>, in the languages the user works in. Load even when the
  user doesn't name the author, as long as the task is in <domain>.
---

# <Author> — Working Knowledge

> Synthesized across <N> books by <Author>. Cross-book frameworks and through-lines
> live here; for a specific book's full treatment, load its map under
> `references/books/<slug>/`.

## Core project
[2-4 sentences: the throughline intellectual project uniting the work — what this
author is fundamentally trying to do or figure out across all the books.]

## Cross-book frameworks (canonical)
[Frameworks recurring across ≥2 books (or single-book pillars). Canonical name +
gloss + which books + variant notes + depth pointer. 6-12 items.]
1. **<Framework>** — <canonical gloss>. In <BookA, BookD>; <BookD> adds <variant>.
   Depth: `references/books/<slug>/chapters/<file>.md`.
   ...

## Through-lines & worldview
[Recurring themes/commitments — or an honest statement that the work is eclectic and
the constant is a method/temperament, not a doctrine.]

## Evolution timeline
[Publication order: BookA (yr) introduced X → BookB (yr) refined → BookD (yr)
reversed Y. Requires years; omit or weaken if unknown.]

## Method & voice
[How the author argues: evidence types, rhetorical moves, chapter structure, stance.
Orthogonal to content; the key to emulating their thinking.]

## Bibliography & reading map
- **<Book> (yr)** → `references/books/<slug>/map.md` — <what it's for; read when…; pairs with…>.
  ...
Suggested reading order: <…>.

## How to use this skill
For a framework, this map gives the canonical form; load the book map + chapter
toolkit named in its depth pointer for the full treatment. For a single book's
argument, load that book's map. Priority of the author's principles (on conflict): <…>.
```

---

## Worked micro-example (abbreviated)

```markdown
## Cross-book frameworks (canonical)
1. **Just-in-time organization** — organize information at the moment of use, by
   actionability, not upfront by topic. Central in *Second Brain*; foreshadowed in
   the earlier essays as "the PARA instinct." Depth:
   `references/books/second-brain/chapters/ch05-organize-para.md`.

## Evolution timeline
- 2017 essays introduce progressive summarization as a blogging habit →
- 2022 *Building a Second Brain* systematizes it into the CODE method →
- 2023 *The PARA Method* extracts organization into a standalone book, narrowing
  scope but deepening the actionability principle.
```

---

## Quality bar for Tier 0

- **Routes across books**, not just within one. If Claude can't tell which book to
  open for depth, the map failed.
- **Canonical + variants**, not a pile of per-book frameworks re-listed.
- **Honest about coherence** — no manufactured grand theory.
- **Dated evolution** or none. **Paraphrase** throughout; no verbatim reproduction.

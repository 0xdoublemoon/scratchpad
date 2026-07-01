# Tier 1 — Concept Map Template (the generated skill's SKILL.md)

This is the **always-loaded** layer. It must give Claude enough to (a) answer
shallow questions and orient itself, and (b) know *which* chapter toolkit to
pull for depth. Budget: **~3,000 tokens** for the body. Be dense, not chatty.

Copy this structure exactly. Replace bracketed guidance with distilled content.

---

```markdown
---
name: <book-slug>            # kebab-case, derived from the title, e.g. "thinking-in-systems"
description: >
  <One line on what knowledge this skill encodes> Use this skill whenever the
  user <specific tasks the book helps with — derived from the book's domain>.
  Triggers include: <5-8 concrete phrases a user would say, in the languages the
  user works in>. Load this even when the user doesn't name the book, as long as
  the task falls in <domain>.
---

# <Book Title> — Working Knowledge

> Distilled from *<Title>* by <Author>. This encodes the book's reusable
> thinking, not a summary. For depth on any area, load the matching chapter
> toolkit from `references/`.

## Thesis
[2-4 sentences. The single load-bearing argument of the whole book — the thing
everything else serves. Not "this book is about X"; state the actual claim.]

## Load-bearing frameworks
[6-10 frameworks. These are the mental models the book returns to again and
again — the scaffolding you'd reuse to think a new problem through. For each:
**name** — 1-3 sentence gloss of what it is and what it's for. Keep the author's
own vocabulary. Skip incidental models that appear once.]

1. **<Framework name>** — <what it is, when it applies>.
2. **<Framework name>** — <...>.
   ... (6-10 total)

## Chapter index
[One line per chapter toolkit: number, title, and the trigger for loading it —
"when the user is dealing with X, load this." This is a routing table.]

- **01 · <Chapter title>** → `references/01-<slug>.md` — load when <situation>.
- **02 · <Chapter title>** → `references/02-<slug>.md` — load when <situation>.
  ...

## Topic index
[Alphabetical-ish map from concept/term → chapter toolkit that covers it. This
lets Claude jump straight to depth on a keyword without rereading the map.
Include the book's signature terms and any synonym a user might say.]

- <concept / term> → ch. NN
- <concept / term> → ch. NN
  ...

## How to use this skill
When a task touches one of the topics above, read the matching
`references/NN-<slug>.md` toolkit before answering — it carries the frameworks,
step-by-step techniques, anti-patterns, and worked examples that this map only
names. Do not answer complex application questions from this map alone.
```

---

## Worked micro-example (abbreviated)

```markdown
## Thesis
Persistent problems are usually produced by the *structure* of a system, not by
bad actors within it. Change the stocks, flows, and feedback loops and behavior
changes on its own; blame the individuals and the structure regenerates the
problem.

## Load-bearing frameworks
1. **Stock & flow** — a stock is an accumulation (water in a tub); flows are the
   rates that fill or drain it. Most intuition errors come from confusing the
   two, so model any dynamic situation as stocks changed by flows first.
2. **Balancing vs. reinforcing loops** — balancing loops seek a goal and create
   stability; reinforcing loops amplify and create growth or collapse. Identify
   which dominates to predict a system's behavior over time.
   ... (6-10 total)

## Chapter index
- **03 · Leverage points** → `references/03-leverage-points.md` — load when the
  user wants to intervene in a system and needs to know where a small push pays.
```

---

## Quality bar for Tier 1

- **Routing over recall.** If Claude can't tell from this map *which* toolkit to
  open for a given question, the map has failed its main job.
- **Frameworks must be load-bearing** — reused across the book, not one-off.
- **Author's vocabulary preserved** so the topic index actually matches how the
  book (and its readers) name things.
- **No padding.** Every line earns its token budget. Cut throat-clearing.
- **Paraphrase, don't transcribe.** State frameworks in compressed form; never
  paste long verbatim passages from the book.

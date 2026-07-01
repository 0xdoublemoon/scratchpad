# Tier 2 — Chapter Toolkit Template (`references/NN-<slug>.md`)

This is the **on-demand** layer, loaded only when the concept map routes a task
here. It must be *operational*: enough to actually apply the chapter's ideas,
not to recount them. Budget: **~1,000 tokens each** (hard ceiling ~1,200).

One toolkit per conceptual unit. Usually that maps 1:1 to a chapter, but:
- **Merge** tiny front/back matter (preface, acknowledgments) — don't give them
  a toolkit at all.
- **Split** a very long chapter that carries two distinct methods into two.
- **Rename** to the concept, not the book's cute chapter title, if that aids
  routing (keep the original title in a subtitle line).

Copy this structure exactly.

---

```markdown
# <NN> · <Chapter / concept title>
> <original chapter title if renamed> · from *<Book Title>*

**Core idea:** [1-2 sentences — the one thing this chapter adds to the thesis.]

## Frameworks
[The specific models/structures introduced here, stated so they can be applied.
If a framework has steps or components, list them. 2-4 items.]
- **<name>** — <what it is> → <how it decomposes / its parts>.

## Techniques
[Concrete, do-this moves. Imperative voice. These are the "how", the actions a
reader would take. 3-6 items.]
- <Do X by doing Y when Z.>

## Anti-patterns
[What the book explicitly warns against, or the failure modes it diagnoses.
Name the mistake + why it fails + the correction. 2-5 items.]
- **<name of mistake>** — <why it fails>; instead, <correction>.

## Worked examples
[1-2 condensed illustrations showing a framework/technique applied end to end.
Paraphrase and compress the book's example, or synthesize a faithful one. Show
the reasoning, not just the conclusion. Keep each to a short paragraph.]
- *<setup>* → applying <framework>, <the move> → <outcome and why>.
```

---

## Worked micro-example (abbreviated)

```markdown
# 03 · Leverage points
> "Places to Intervene in a System" · from *Thinking in Systems*

**Core idea:** Interventions differ enormously in power. The obvious levers
(parameters, subsidies) are weak; the deep ones (goals, paradigms, rules) are
strong but harder to move.

## Frameworks
- **Leverage ladder** — a ranked list of intervention points, weakest
  (constants/parameters) to strongest (the power to transcend paradigms). Locate
  your proposed fix on the ladder before committing to it.

## Techniques
- Before tuning a number, ask whether the *rule* or *goal* producing that number
  is the real lever — moving up the ladder usually beats optimizing down it.
- Map who controls each leverage point; a strong lever no one can move is inert.

## Anti-patterns
- **Parameter obsession** — endlessly tweaking taxes/rates (weak levers) while
  the system's goal stays untouched; instead, target the goal or the rules.
- **Backwards intervention** — pushing a strong lever in the wrong direction
  because system counterintuitiveness wasn't checked first.

## Worked examples
- *A city fights congestion by widening roads* → applying the leverage ladder,
  road width is a low parameter-level lever; induced demand refills it. The
  higher lever is the *goal* ("move cars fast" → "move people well"), which
  reframes toward transit/pricing and actually shifts behavior.
```

---

## Quality bar for Tier 2

- **Operational, not recap.** A reader should be able to *act* from this toolkit.
- **All four sections present** (frameworks, techniques, anti-patterns, worked
  examples). If the chapter genuinely lacks one, write "— none distinct —" rather
  than padding, but first look harder: most how-to chapters have all four.
- **Compress hard** to hit ~1K tokens; drop anecdote and repetition, keep the
  reusable skeleton and the author's terms.
- **Paraphrase examples.** Never reproduce long verbatim passages; distill the
  book's illustration into your own compressed retelling.

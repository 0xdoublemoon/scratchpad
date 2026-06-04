---
name: svg-logo
description: >
  Generate a production-ready SVG logo mark (50×50, icon only, no text).
  Use this skill whenever the user asks to create a logo, icon, brand mark, app icon, or favicon.
  Trigger on phrases like "make me a logo", "design an icon", "create a brand mark", "logo for X".
  Always ask for style and color palette before generating.
---

# SVG Logo Skill

Generates a clean, standalone SVG logo mark. Always icon-only — no brand name text.

## Canvas

```
viewBox="0 0 100 100"   width="100"   height="100"
Safe zone: all elements within 6,6 → 94,94
```

---

## Step 1 — Collect Options

Use `ask_user_input_v0` with these two questions before generating.
Skip any option the user already specified in their message.

```
Q1 (single_select): Style
  Options: Geometric | Lettermark | Abstract mark | Mascot/character

Q2 (single_select): Color palette  [primary + accent]
  "Midnight"   → #1E1B4B + #818CF8   (deep navy + soft indigo)
  "Ember"      → #7C2D12 + #FB923C   (dark brown + vivid orange)
  "Moss"       → #14532D + #4ADE80   (dark green + bright mint)
  "Steel"      → #0F172A + #38BDF8   (near-black + sky blue)
  "Blush"      → #831843 + #F9A8D4   (deep rose + pale pink)
  "Obsidian"   → #1C1917 + #A8A29E   (near-black + warm gray)

Q3 (single_select): Animation
  Options: None (static) | Entrance (fade/scale in) | Loop (breathe/pulse) | Spin (continuous rotate)
```

---

## Step 2 — Generate SVG

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <title>{Brand or concept name}</title>
  <desc>{One-line description}</desc>
  <!-- mark geometry centered near 50,50 -->
</svg>
```

**Design rules:**
- 1–2 colors maximum (primary + accent from chosen palette)
- Use geometric primitives: `<circle>`, `<rect>`, `<polygon>`, `<path>`
- Composition must read clearly at 50×50 — no fine detail
- Works on both light and dark backgrounds
- No external resources, no fonts, no JavaScript

**Style guidance:**
| Style | Approach |
|---|---|
| Geometric | Circles, triangles, hexagons — clean mathematical shapes |
| Lettermark | Single letter or initials as the shape itself |
| Abstract mark | Non-literal shape suggesting a concept or feeling |
| Mascot/character | Simplified character, face, or creature using basic shapes |

---

## Step 3 — Add Animation (if requested)

Use SMIL `<animate>` or CSS `@keyframes` inside `<style>`. No JavaScript.

**Entrance — fade + scale in (plays once on load):**
```xml
<style>
  .mark { animation: enter 0.6s ease-out both; }
  @keyframes enter { from { opacity:0; transform:scale(0.6); } to { opacity:1; transform:scale(1); } }
</style>
```

**Loop — breathe/pulse (repeats forever):**
```xml
<style>
  .mark { animation: breathe 2.4s ease-in-out infinite; transform-origin: 50px 50px; }
  @keyframes breathe { 0%,100% { transform:scale(1); } 50% { transform:scale(1.08); } }
</style>
```

**Spin — continuous rotation:**
```xml
<animateTransform attributeName="transform" type="rotate"
  from="0 50 50" to="360 50 50" dur="3s" repeatCount="indefinite"/>
```

Animation rules:
- Apply animation class/element only to the main mark group, not the whole SVG
- Keep durations natural: entrance 0.4–0.8s, loops 1.5–3s, spin 2–4s
- Entrance animations use `animation-fill-mode: both` so they don't flash on load

---

## Output

Save to `./outputs/{name}-logo.svg` and present the file.
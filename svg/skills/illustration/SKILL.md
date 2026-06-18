---
description: >
  Generate a production-ready SVG illustration (400×300 default canvas).
  Use this skill whenever the user asks to draw, illustrate, or create a scene, concept art, spot art,
  hero graphic, or decorative visual. Trigger on phrases like "illustrate X", "draw a scene of X",
  "create a graphic for X", "make an illustration", "hero image for X".
  Always ask for style, palette, canvas size, and animation before generating.
---

# SVG Illustration Skill

Generates expressive, layered SVG illustrations. Fully self-contained — no external resources.

## Canvas Options

| Option | viewBox | Use for |
|---|---|---|
| Landscape (default) | `0 0 400 300` | Docs, cards, general purpose |
| Wide banner | `0 0 800 400` | Hero sections, headers |
| Portrait | `0 0 400 500` | Mobile, posters |
| Square | `0 0 400 400` | Social media, tiles |

---

## Step 1 — Collect Options

Use `ask_user_input_v0` before generating. Skip anything already specified by the user.

```
Q1 (single_select): Visual style
  Options: Flat | Outlined | Isometric | Organic

Q2 (single_select): Color palette  [primary + secondary + accent + background]
  "Aurora"   → #6D28D9 + #0EA5E9 + #F472B6 + #F5F3FF   (purple, sky, pink, lavender bg)
  "Meadow"   → #15803D + #65A30D + #FCD34D + #F0FDF4   (forest, lime, gold, mint bg)
  "Dusk"     → #1D4ED8 + #7C3AED + #F97316 + #EFF6FF   (blue, violet, orange, light bg)
  "Sand"     → #92400E + #D97706 + #FDE68A + #FFFBEB   (brown, amber, cream, warm bg)
  "Coral"    → #BE185D + #EA580C + #FCD34D + #FFF1F2   (rose, orange, yellow, blush bg)
  "Arctic"   → #0C4A6E + #0E7490 + #67E8F9 + #F0F9FF   (navy, teal, ice, pale bg)

Q3 (single_select): Canvas size
  Options: Landscape 400×300 | Wide banner 800×400 | Portrait 400×500 | Square 400×400

Q4 (single_select): Animation
  Options: None (static) | Float (gentle up/down drift) | Fade in layers | One element loops
```

---

## Step 2 — Generate SVG

Structure every illustration in three layers (back to front):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <title>{Subject}</title>
  <desc>{One-sentence description}</desc>
  <defs>
    <!-- gradients, clipPaths if needed -->
  </defs>

  <!-- Layer 1: Background — sky, ground, abstract fill -->
  <g id="background"> ... </g>

  <!-- Layer 2: Mid-ground — supporting objects, context -->
  <g id="midground"> ... </g>

  <!-- Layer 3: Foreground — main subject, focal element -->
  <g id="foreground"> ... </g>
</svg>
```

**Style guidance:**
| Style | Technique |
|---|---|
| Flat | Solid fills, no stroke or minimal 1px stroke, bold simple shapes |
| Outlined | Stroked paths 1.5–2px, limited fills, sketch-like |
| Isometric | 30° projection: horizontal lines stay flat, vertical lines angle ±30° |
| Organic | Bezier curves, irregular shapes, nature-inspired forms |

**Color discipline:**
- Background layer: always use the background color from the chosen palette
- Mid-ground: secondary color + lighter tints
- Foreground: primary + accent colors for focal elements
- Max 5 distinct hues total, use opacity variations before adding new colors

**Common patterns:**
- Person/character → circle head + simplified body, no facial detail required
- Device/screen → rounded rect with inner UI suggestion
- Abstract concept (growth, connection, data) → metaphor shapes: arrows, nodes, plants, gears
- Nature scene → layered horizon bands, simple tree/cloud silhouettes

---

## Step 3 — Add Animation (if requested)

Use SMIL or CSS `@keyframes`. No JavaScript. Max 2 animated elements to avoid visual chaos.

**Float — gentle drift (good for clouds, characters, icons):**
```xml
<style>
  .float { animation: float 3s ease-in-out infinite; transform-origin: center; }
  @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
</style>
```

**Fade in layers — background first, then mid, then foreground:**
```xml
<style>
  #background { animation: fadeIn 0.5s ease both; }
  #midground  { animation: fadeIn 0.5s 0.3s ease both; }
  #foreground { animation: fadeIn 0.5s 0.6s ease both; }
  @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
</style>
```

**One element loops — e.g. a spinning gear, pulsing dot:**
```xml
<animateTransform attributeName="transform" type="rotate"
  from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/>
```

Animation rules:
- Float duration: 2.5–4s for calm feel
- Entrance stagger: 0.2–0.4s delay between layers
- Never animate background layer on loop — too distracting
- Keep `transform-origin` explicit to avoid cross-browser jump

---

## Output

Save to `./outputs/{subject}-illustration.svg` and present the file.

---
description: >
  Generate a production-ready SVG flowchart or process diagram (800px wide, auto height).
  Use this skill whenever the user asks to diagram, map, or visualize a process, workflow, decision tree,
  system flow, or step-by-step sequence. Trigger on phrases like "flowchart for X", "diagram the process of X",
  "map out how X works", "create a workflow", "show the steps of X", "decision tree for X".
  Always ask for diagram type, direction, and color palette before generating.
---

# SVG Flowchart Skill

Generates clear, structured SVG flowcharts. Fixed 800px width, height computed from content.

## Canvas

```
viewBox="0 0 800 {computed_height}"   width="800"
Height = (node_count × row_height) + top_padding + bottom_padding
Typical row_height: 80–100px
```

---

## Step 1 — Collect Options

Use `ask_user_input_v0` before generating. Skip anything already specified by the user.

```
Q1 (single_select): Diagram type
  Options: Linear steps | Decision tree (with branches) | Swimlane (by role/team) | Cycle/loop

Q2 (single_select): Flow direction
  Options: Top → Bottom | Left → Right

Q3 (single_select): Color palette  [process node + decision node + background]
  "Indigo"   → #EEF2FF + #FEF9C3 + #F8FAFC   (indigo fill, yellow decisions, cool bg)
  "Ocean"    → #E0F2FE + #ECFDF5 + #F0F9FF   (sky fill, green decisions, white-blue bg)
  "Slate"    → #F1F5F9 + #FFF7ED + #FFFFFF   (gray fill, orange decisions, white bg)
  "Violet"   → #F5F3FF + #FDF2F8 + #FAFAFA   (purple fill, pink decisions, neutral bg)
  "Mono"     → #F1F5F9 + #E2E8F0 + #FFFFFF   (all grays, zero color distraction)
```

---

## Step 2 — Generate SVG

Always define the arrow marker in `<defs>`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}" width="800">
  <title>{Process name}</title>
  <desc>{One-line description}</desc>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#6B7280"/>
    </marker>
  </defs>

  <!-- background rect -->
  <rect width="800" height="{h}" fill="{bg-color}"/>

  <!-- nodes and connectors -->
</svg>
```

---

## Node Shapes & Sizing

| Node type | Shape | SVG | Size |
|---|---|---|---|
| Process step | Rounded rect | `<rect rx="6">` | 200×44px |
| Decision | Diamond | `<polygon>` | 160×60px |
| Start / End | Stadium (pill) | `<rect rx="22">` | 160×44px |
| Input / Output | Parallelogram | `<polygon>` | 200×44px |
| Sub-process | Rect with side bars | `<rect>` + 2 lines | 200×44px |

**Node styling:**
```xml
<!-- Process node -->
<rect fill="{process-color}" stroke="{process-color-dark}" stroke-width="1.5" rx="6"/>

<!-- Decision node -->
<polygon fill="{decision-color}" stroke="{decision-color-dark}" stroke-width="1.5"/>

<!-- Terminal (start/end) -->
<rect fill="#1E293B" rx="22"/>
<text fill="#FFFFFF">...</text>
```

**Text styling (all nodes):**
```xml
<text font-family="system-ui,sans-serif" font-size="13" fill="#1F2937"
      text-anchor="middle" dominant-baseline="middle">Label</text>
```

---

## Layout Algorithms

### Top → Bottom (default)
- Start node: `cx=400, y=40`
- Each row: increment `y` by `90px`
- Node centered at `x=400`, width 200px → `x=300`
- Decision branches: left branch `cx=200`, right branch `cx=600`
- Reconnect branches back to `cx=400` after divergence
- Total height = last node bottom + 60px

### Left → Right
- Start node: `cy=200, x=40`
- Each column: increment `x` by `180px`
- Node centered at `y=200`, height 44px
- Decision branches: top `cy=100`, bottom `cy=300`
- Canvas height = 400px, width = computed

### Swimlane
- Divide 800px into N equal lanes (one per role/team)
- Lane header: 800/N wide × 40px tall, `fill="#E2E8F0"`
- Nodes stay within their lane's x-range
- Cross-lane connectors use curved paths: `<path d="M x1,y1 C mx,my mx,my x2,y2"/>`

### Cycle/Loop
- Arrange nodes in a circle or oval
- Use curved connectors following the arc
- Last node connects back to first with a labeled arrow

---

## Connector Lines

```xml
<!-- Straight vertical connector -->
<line x1="400" y1="{node_bottom}" x2="400" y2="{next_node_top}"
      stroke="#9CA3AF" stroke-width="1.5" marker-end="url(#arrow)"/>

<!-- Branch label (Yes/No) -->
<text x="{mid_x}" y="{mid_y}" font-size="11" fill="#6B7280"
      text-anchor="middle">Yes</text>

<!-- Curved reconnect -->
<path d="M 200,{y} Q 200,{y+40} 400,{y+40}"
      fill="none" stroke="#9CA3AF" stroke-width="1.5" marker-end="url(#arrow)"/>
```

---

## Output

Save to `./outputs/{process-name}-flowchart.svg` and present the file.

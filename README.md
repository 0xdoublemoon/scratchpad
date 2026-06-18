# doublemoon-skills

A Claude Code plugin marketplace with SVG generation skills.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add 0xdoublemoon/scratchpad
```

Then install the SVG plugin:

```
/plugin install svg@doublemoon-skills
```

After installing, run `/reload-plugins` to activate.

## Skills

| Skill | Invoke | Description |
|-------|--------|-------------|
| `logo` | `/svg:logo` | Generate a production-ready SVG logo mark (icon only, 100×100, optional animation) |
| `flowchart` | `/svg:flowchart` | Generate an SVG flowchart or process diagram (800px wide, auto height) |
| `illustration` | `/svg:illustration` | Generate an SVG illustration or scene (400×300 default, multiple canvas options) |

## Local development

Test the plugin without installing:

```bash
claude --plugin-dir ./svg
```

## License

MIT

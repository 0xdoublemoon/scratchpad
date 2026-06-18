# doublemoon-skills

A Claude Code plugin marketplace with SVG generation skills.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add 0xdoublemoon/scratchpad
```

Then install individual skills (or all three):

```
/plugin install svg-logo@doublemoon-skills
/plugin install svg-flowchart@doublemoon-skills
/plugin install svg-illustration@doublemoon-skills
```

After installing, run `/reload-plugins` to activate.

## Skills

| Skill | Invoke | Description |
|-------|--------|-------------|
| `svg-logo` | `/svg-logo:svg-logo` | Generate a production-ready SVG logo mark (icon only, 100×100, optional animation) |
| `svg-flowchart` | `/svg-flowchart:svg-flowchart` | Generate an SVG flowchart or process diagram (800px wide, auto height) |
| `svg-illustration` | `/svg-illustration:svg-illustration` | Generate an SVG illustration or scene (400×300 default, multiple canvas options) |

## Local development

Test a plugin without installing:

```bash
claude --plugin-dir ./svg-logo
```

## License

MIT

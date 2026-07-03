# doublemoon-skills

A Claude Code plugin marketplace with SVG generation and stock analysis skills.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add 0xdoublemoon/scratchpad
```

Then install the plugins you want:

```
/plugin install svg@doublemoon-skills
/plugin install stock@doublemoon-skills
```

After installing, run `/reload-plugins` to activate.

## Skills

### svg

| Skill | Invoke | Description |
|-------|--------|-------------|
| `logo` | `/svg:logo` | Generate a production-ready SVG logo mark (icon only, 100×100, optional animation) |
| `flowchart` | `/svg:flowchart` | Generate an SVG flowchart or process diagram (800px wide, auto height) |
| `illustration` | `/svg:illustration` | Generate an SVG illustration or scene (400×300 default, multiple canvas options) |

### stock

Requires [IBKR MCP](https://github.com/anthropics/claude-plugins-official) for real-time price data.

| Skill | Invoke | Description |
|-------|--------|-------------|
| `analysis` | `/stock:analysis` | Structured Buy/Hold/Sell report with fundamentals, valuation, technicals, and risk factors |
| `screener` | `/stock:screener` | Screen and filter US stocks based on criteria |

## Local development

Test a plugin without installing:

```bash
claude --plugin-dir ./svg
claude --plugin-dir ./stock
```

## License

MIT

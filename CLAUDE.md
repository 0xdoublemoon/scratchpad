# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a Claude Code plugin marketplace — it contains a single `svg` plugin with three SVG generation skills. There is no build system, test runner, or application to run; the "code" is the skill definition files themselves.

## Repository Structure

```
.claude-plugin/
  marketplace.json          # Marketplace catalog listing the svg plugin
svg/
  .claude-plugin/
    plugin.json             # Plugin manifest (name: "svg")
  skills/
    logo/
      SKILL.md              # SVG logo mark skill
    flowchart/
      SKILL.md              # SVG flowchart skill
    illustration/
      SKILL.md              # SVG illustration skill
stock/
  .claude-plugin/
    plugin.json             # Plugin manifest (name: "stock")
  skills/
    analysis/
      SKILL.md              # US stock analysis skill
    screener/
      SKILL.md              # Stock screener skill
outputs/                    # Sample/test SVG output (not part of skill definitions)
```

## Plugin Manifest Format

`.claude-plugin/plugin.json` defines the plugin:

```json
{
  "name": "svg",
  "description": "...",
  "version": "1.0.0",
  "author": { "name": "0xdoublemoon" }
}
```

## Marketplace Catalog

`.claude-plugin/marketplace.json` lists the plugin with its source path:

```json
{
  "name": "doublemoon-skills",
  "owner": { "name": "0xdoublemoon" },
  "plugins": [
    { "name": "svg", "source": "./svg", "description": "..." }
  ]
}
```

## Skill File Format

Each `SKILL.md` begins with YAML frontmatter:

```yaml
---
description: >
  One-paragraph description used for skill matching and triggering.
  Include trigger phrases here so Claude knows when to invoke this skill.
---
```

The skill name comes from the directory name (e.g. `skills/logo/` → `/svg:logo`). Do not add `name:` to the frontmatter.

The body describes how Claude should execute the skill — canvas specs, step-by-step generation instructions, output naming conventions, etc.

## Output Convention

Generated SVG files are saved to `./outputs/{name}-{type}.svg` (e.g. `outputs/brew-logo.svg`). The `outputs/` directory is for test/sample output and is not part of the skill definitions.

## SVG Skill Defaults

| Skill | Invocation | Canvas | Center |
|---|---|---|---|
| logo | `/svg:logo` | 100×100, safe zone 6,6→94,94 | 50,50 |
| flowchart | `/svg:flowchart` | 800px wide, height computed | — |
| illustration | `/svg:illustration` | 400×300 default (landscape) | — |
| analysis | `/stock:analysis` | US stock Buy/Hold/Sell report | — |
| screener | `/stock:screener` | US stock screener | — |

When modifying animation coordinates in the logo skill, the breathe `transform-origin` and spin rotation center must both reference `50px 50px` / `50 50`.

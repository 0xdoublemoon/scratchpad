# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a Claude Code plugin marketplace — it contains three SVG generation skills distributed as installable plugins. There is no build system, test runner, or application to run; the "code" is the skill definition files themselves.

## Repository Structure

```
.claude-plugin/
  marketplace.json          # Marketplace catalog listing all three plugins
svg-logo/
  .claude-plugin/
    plugin.json             # Plugin manifest for svg-logo
  skills/
    svg-logo/
      SKILL.md              # Skill definition
svg-flowchart/
  .claude-plugin/
    plugin.json
  skills/
    svg-flowchart/
      SKILL.md
svg-illustration/
  .claude-plugin/
    plugin.json
  skills/
    svg-illustration/
      SKILL.md
outputs/                    # Sample/test SVG output (not part of skill definitions)
```

## Plugin Manifest Format

Each plugin has a `.claude-plugin/plugin.json`:

```json
{
  "name": "svg-logo",
  "description": "...",
  "version": "1.0.0",
  "author": { "name": "0xdoublemoon" }
}
```

## Marketplace Catalog

`.claude-plugin/marketplace.json` lists all plugins with their local source paths:

```json
{
  "name": "doublemoon-skills",
  "owner": { "name": "0xdoublemoon" },
  "plugins": [
    { "name": "svg-logo", "source": "./svg-logo", "description": "..." }
  ]
}
```

**Every plugin directory must be listed here with a `source` field.**

## Skill File Format

Each `SKILL.md` begins with YAML frontmatter:

```yaml
---
description: >
  One-paragraph description used for skill matching and triggering.
  Include trigger phrases here so Claude knows when to invoke this skill.
---
```

The skill name comes from the directory name (e.g. `skills/svg-logo/` → `svg-logo`), not from a `name:` field. Do not add `name:` to the frontmatter.

The body describes how Claude should execute the skill — canvas specs, step-by-step generation instructions, output naming conventions, etc.

## Output Convention

Generated SVG files are saved to `./outputs/{name}-{type}.svg` (e.g. `outputs/brew-logo.svg`). The `outputs/` directory is for test/sample output and is not part of the skill definitions.

## SVG Skill Defaults

| Skill | Canvas | Center |
|---|---|---|
| `svg-logo` | 100×100, safe zone 6,6→94,94 | 50,50 |
| `svg-flowchart` | 800px wide, height computed | — |
| `svg-illustration` | 400×300 default (landscape) | — |

When modifying animation coordinates in `svg-logo`, the breathe `transform-origin` and spin rotation center must both reference `50px 50px` / `50 50`.

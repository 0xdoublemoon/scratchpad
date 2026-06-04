# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a Claude Code plugin marketplace — it contains custom Claude Code skills distributed as a plugin package. There is no build system, test runner, or application to run; the "code" is the skill definition files themselves.

## Plugin Structure

Skills are defined as Markdown files with YAML frontmatter and registered in `.claude-plugin/marketplace.json`. Each skill lives in its own directory:

```
svg-logo/svg-logo.md
svg-flowchart/svg-flowchart.md
svg-illustration/svg-illustration.md
```

**Registration:** Every skill directory and path must be listed in `.claude-plugin/marketplace.json` under `"plugins"`. A skill file that isn't registered will not be recognized by Claude Code.

## Skill File Format

Each `*.md` skill file must begin with YAML frontmatter:

```yaml
---
name: skill-name          # must match the "name" field in marketplace.json
description: >
  One-paragraph description used for skill matching and triggering.
  Include trigger phrases here so Claude knows when to invoke this skill.
---
```

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

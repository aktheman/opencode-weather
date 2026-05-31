# AGENTS.md — opencode

Personal opencode configuration: agents, skills, MCP servers, permissions,
and workspace-level settings.

## Commands

- `python main.py` — prints `Hei fra OpenCode` (smoke test / placeholder)

## What belongs here

- `opencode.json` / `opencode.jsonc` — workspace-level config
- `.opencode/` — agents, skills, MCP servers, permission rules
- `~/.config/opencode/` — user-global config (outside this repo)

## Workflow

- Load the `customize-opencode` skill before editing any opencode config files.
- Commit config changes back to this repo after adding/modifying agents, skills,
  or permissions.

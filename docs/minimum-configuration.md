# Minimum usable configuration — paraqualis-gxp

The single page that says **what must be in place for the toolkit to work**, and the one
step that satisfies each. (Closes gap GOQ-007.)

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## Prerequisites

| Requirement | Why | How to satisfy |
|---|---|---|
| **Claude Code** | Host for the commands, skills, agents, hook, and MCP server | Install Claude Code |
| **Python ≥ 3.10** | The openFDA MCP server depends on the `mcp` SDK, which does **not** support Python 3.9 (the Word/Excel builders run on 3.9+, but 3.10+ is the project target) | `brew install python@3.12` (macOS) or your platform's installer |
| **Python dependencies** | `python-docx`, `openpyxl` (Word/Excel rendering) and `mcp` (openFDA server) | `pip install -r requirements.txt` — ideally into a virtualenv (`python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt`) |
| **openFDA API key** *(optional)* | Only raises the rate limit (~1,000 → ~120,000 req/day); every tool works without it | `/openfda:setup`, or set `OPENFDA_API_KEY` in the environment / `.env` |

## How each component is enabled

| Component | Plugin install | Source / dev install |
|---|---|---|
| **Commands / skills / sub-agents** | Auto-loaded when the plugin is installed | `./install.sh` symlinks them into `~/.claude/` |
| **Document-protection hook** | Auto-discovered from `hooks/hooks.json` (`${CLAUDE_PLUGIN_ROOT}`) — active automatically | **Opt-in:** add the `PreToolUse` block from `hooks/README.md` to `~/.claude/settings.json` (user) or `<repo>/.claude/settings.json` (project, via `${CLAUDE_PROJECT_DIR}`). The hook uses only the Python standard library, so any `python3` works. |
| **openFDA MCP server** | Declared in `plugin.json` → `mcpServers` (`${CLAUDE_PLUGIN_ROOT}`); launched with `python3` | Register manually: `claude mcp add openfda -- <python3.10+> "<repo>/mcp-servers/openfda/server.py"` (point at the venv interpreter if your default `python3` is < 3.10) |

> The MCP server runs a **pre-flight check**: if it is launched on Python < 3.10 or without
> the `mcp` package it exits immediately with a clear message telling you to install the
> dependencies — it never starts silently broken. The Word/Excel builders do the same for
> `python-docx` / `openpyxl`.

## Minimum "just works" path

1. Install Python ≥ 3.10 and run `pip install -r requirements.txt`.
2. Install the plugin (`/plugin marketplace add …` then `/plugin install …`) **or** run `./install.sh`.
3. (Optional) `/openfda:setup` for a personal openFDA key.

## Verify

```bash
# dependency + structure checks (read-only)
bash Qualification/scripts/IQ-005-python-packages.sh   # all three importable
bash Qualification/scripts/IQ-002-command-structure.sh # 18 commands valid
claude plugin validate .                               # plugin manifest valid
```

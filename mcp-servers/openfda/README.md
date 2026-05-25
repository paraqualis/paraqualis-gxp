# openFDA MCP server

Exposes the FDA open data API (`api.fda.gov`) to Claude as **tools** — real functions
Claude calls directly (with structured inputs/outputs), instead of fetching ad-hoc. This
is the "tool" tier: actual code, not a prompt.

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## What it gives Claude

| Tool | What it does |
|---|---|
| `search_enforcement(category, search, limit)` | FDA recall / enforcement reports for `drug`, `device`, or `food` |
| `search_drug_labels(search, limit)` | Structured drug labeling (brand/generic/manufacturer, indications, warnings, dosage) |
| `search_drug_adverse_events(search, limit)` | FAERS adverse-event reports (reactions + drugs per report) |
| `openfda_query(endpoint, search, limit)` | Generic escape hatch for any other endpoint (e.g. `device/510k`, `drug/ndc`) |

Results are trimmed to the useful fields so responses stay compact.

## One-time setup

```bash
pip install mcp        # the only dependency; HTTP uses the Python standard library
```

**API key (optional but recommended):** the server reads `OPENFDA_API_KEY` from the
environment if present — it only raises the rate limit (~1,000 → ~120,000 requests/day);
the tools work without one. Get/configure a free key with the **`/openfda:setup`** command.
Because the key lives in your shell environment, Claude Code passes it through to the server.

## Register it with Claude Code

**User scope (available in every project):**
```bash
claude mcp add openfda --scope user -- python3 "<repo>/mcp-servers/openfda/server.py"
```
Replace `<repo>` with the absolute path to this repository.

**Or project scope** — drop a `.mcp.json` at a project root:
```json
{
  "mcpServers": {
    "openfda": { "command": "python3", "args": ["<repo>/mcp-servers/openfda/server.py"] }
  }
}
```

Restart Claude Code. The four tools then appear to Claude like the built-in tools — ask
in plain English (e.g. *"any Class I drug recalls for insulin pumps this year?"*) and
Claude calls the right tool.

## openFDA query syntax (quick reference)

- Field match: `field:value` — e.g. `classification:"Class I"`, `recalling_firm:"Acme"`
- AND / OR: join with `+AND+` / `+OR+`
- Date range: `field:[20240101+TO+20241231]`
- Full field list per endpoint: <https://open.fda.gov/apis/>

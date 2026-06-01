# Security Policy

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## Reporting a vulnerability

If you find a security issue in **paraqualis-skills** — anything that could be
exploited to read or alter data outside the toolkit's intended scope, escape
the document-protection hook, leak credentials, or compromise a host running
the openFDA MCP server — please report it **privately** rather than opening a
public issue.

**Contact:** `craig@paraqualis.com` (subject line: "paraqualis-skills security")

We aim to:
- Acknowledge your report within **5 working days**.
- Provide an initial assessment within **10 working days**.
- Coordinate a fix, a release, and (with your permission) credit you in the
  release notes.

Please include:
- A clear description of the issue and its impact.
- The shortest reproducer you can produce.
- The version (or commit SHA) you observed it on.

Do **not** include real openFDA API keys, FDA Data Dashboard credentials, or
any personally-identifying information in your report. We will not act on
reports that depend on already-public credentials.

## Scope

**In scope:**
- The plugin itself (commands, skills, sub-agents, hooks) shipped in this repository.
- The openFDA MCP server in `mcp-servers/openfda/`.
- The supplied build scripts (`docs/build_*.py`, `qualification-pack-template/build_*.py`)
  and git hooks (`.githooks/pre-commit`).

**Out of scope:**
- Vulnerabilities in upstream services (openFDA, eCFR, Anthropic Claude Code itself,
  Python, OS packages). Please report those to their respective owners.
- Issues that require an attacker to have already obtained your shell or Claude Code
  credentials.
- The *output* of the qualification engine — this is **DRAFT** material requiring
  review and approval by appropriately qualified and authorized personnel before
  any GxP use, and is not a security boundary.

## Supply-chain notes for regulated installers

paraqualis-skills is distributed via Git with tagged releases on
[GitHub](https://github.com/paraqualis/paraqualis-skills). Regulated installers
should:

- **Pin to a tag** (e.g. `v1.0.0`) rather than tracking `main`, so the installed
  version is reproducible and reviewable.
- **Verify the commit SHA** of the tag against the release notes before promoting
  an install to a GxP-relevant environment.
- Treat the toolkit as a **GxP-impacting tool** in its own right — the generator
  of qualification material is itself a candidate for qualification before its
  output is relied upon.

## Hardening posture

- Hooks fail **open** by default (allow on internal error) to avoid wedging a
  Claude Code session in this initial release. Regulated deployments should
  flip the document-protection hook to **fail-closed** — a one-line change in
  `hooks/protect-approved-documents.py` (return `2` on the broad `except`
  paths). See `hooks/README.md`.
- The openFDA MCP server is **opt-in** and is not auto-bundled by the plugin
  manifest. It is registered only after the user runs
  `claude mcp add openfda …` explicitly. The server uses the Python standard
  library for HTTP; the only third-party dependency is `mcp` itself.
- `.env` files are excluded from version control by `.gitignore`. Every commit
  in the public history has been scanned for secret-shaped content prior to
  the v1.0.0 release.

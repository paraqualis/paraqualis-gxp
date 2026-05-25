---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Check for an openFDA API key and, if it's missing, help the user get a free one and save it to a shell file of their choice
argument-hint: (no arguments — just run it)
---

Set up an **openFDA API key** (`OPENFDA_API_KEY`) for the user. openFDA keys are **free,
issued instantly, and not secret** — they only raise the request rate limit (about
1,000 → 120,000 requests/day). Walk the user through this, in plain English.

## 1. Detect whether a key is already configured
- Check the environment: is `OPENFDA_API_KEY` already set and non-empty?
  (`bash -lc 'echo ${OPENFDA_API_KEY:+already-set}'` — show only "already-set", not the value.)
- Also look for an existing entry in the usual files (search by name only, don't print values):
  `~/.bashrc`, `~/.zshrc`, `~/.profile`, `~/.bash_profile`, `~/.env`, and a `.env` in the
  current project.
- **If it's already set or found:** tell the user it's configured and where, optionally
  confirm it works with one harmless call (below), and stop. Nothing else to do.

## 2. If it's missing — guide them to get one (you can't fetch it for them)
Explain plainly that a key is free and takes under a minute, then:
- Send them to **https://open.fda.gov/apis/authentication/**
- They enter an email address and submit; the key is shown on the page and emailed
  **immediately**. (It requires their email on the form, so they have to do this step.)
- Ask them to paste the key back to you when they have it.

## 3. Save it where the user chooses
Ask which file to put it in, and default to the one that matches their shell:
- **bash** → `~/.bashrc` (or `~/.bash_profile` on macOS login shells)
- **zsh** → `~/.zshrc`
- a portable login file → `~/.profile`
- a **project `.env`** if they want it scoped to one project

Then write the line, without duplicating an existing entry (update in place if present):
- shell rc / profile → `export OPENFDA_API_KEY="<key>"`
- `.env` file → `OPENFDA_API_KEY=<key>`

For a project `.env`, make sure `.env` is in `.gitignore` — not because the key is secret
(it isn't), just so it doesn't clutter the repo. Tell the user to run `source <file>` or
open a new terminal for it to take effect.

## 4. Verify
- Reload and confirm `OPENFDA_API_KEY` is now set (show "set", not the value).
- Optionally prove it authenticates with one harmless call and report only the HTTP status:
  `curl -s -o /dev/null -w '%{http_code}\n' "https://api.fda.gov/drug/enforcement.json?limit=1&api_key=$OPENFDA_API_KEY"`
  (200 = working; 401/403 = the key was mistyped).

Lead with whether a key was found. Keep every message plain and short. The key isn't
secret, so don't be heavy-handed about masking — but there's no need to echo it either.

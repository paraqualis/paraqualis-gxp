# Hooks

Claude Code **hooks** are shell commands Claude Code runs automatically at defined
moments in its lifecycle (before a tool runs, after an edit, when you submit a prompt,
when it finishes). Unlike a skill or command, a hook is **deterministic** — it always
fires, regardless of what the model decides. That makes hooks the right place for safety
and governance controls.

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## `protect-approved-documents.py`

A **PreToolUse** hook that refuses any edit to an *approved, locked* document.

A document becomes locked the moment it contains this marker line anywhere in its text:

```
<!-- PARAQUALIS-LOCK: approved -->
```

When Claude tries to edit a file carrying that marker, the hook blocks the tool call and
tells Claude why. Locking is **opt-in per document** and **visible in the document itself**
— which is how a controlled record should behave: the approval is part of the record, and
revising it means a new version under change control, not an in-place overwrite.

- **New files** (not yet on disk) are always allowed — you can create, you just can't
  modify a locked one.
- **Unlocked files** are untouched — the hook only ever triggers on files carrying the marker.

### Register it

**There are three ways the hook gets registered — pick the one matching how you installed:**

1. **As a plugin (recommended):** nothing to do. `hooks/hooks.json` (which uses the
   portable `${CLAUDE_PLUGIN_ROOT}` path) is **auto-discovered** when the plugin is
   installed — the hook is active automatically.
2. **Working inside this repo (dev/dogfood):** the repo ships a project-scoped
   `.claude/settings.json` that registers the hook via `${CLAUDE_PROJECT_DIR}` — active for
   any session opened in this repo.
3. **Manual / source install elsewhere:** add the block below to your own `settings.json`
   — **user scope** (`~/.claude/settings.json`) for machine-wide protection, or **project
   scope** (`<project>/.claude/settings.json`) for one project. Because the marker is opt-in
   per file, user scope is safe — it only bites on files you've locked.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"/ABSOLUTE/PATH/TO/paraqualis-skills/hooks/protect-approved-documents.py\""
          }
        ]
      }
    ]
  }
}
```

This absolute-path form is **only** for the manual/source install (mode 3). For plugin or
in-repo use, prefer the portable path variables instead of a hard-coded path:
`${CLAUDE_PLUGIN_ROOT}/hooks/protect-approved-documents.py` (plugin, as in `hooks/hooks.json`)
or `${CLAUDE_PROJECT_DIR}/hooks/protect-approved-documents.py` (project scope). Keep the
quotes — paths may contain spaces. **Restart Claude Code** (or run `/hooks`) so it picks up
the change.

### Design choice: fail-open vs. fail-closed

This hook **fails open** — if it can't parse the event or read the file, it *allows* the
edit rather than wedge the session. That's the safe default for a learning/utility hook.
For a validated, production deployment protecting real GxP records you would likely flip
it to **fail-closed** (block on any error), so the protection can't be defeated by making
the hook crash. One-line change in the script.

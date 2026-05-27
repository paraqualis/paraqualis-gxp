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

Add this to your `settings.json`. Use **user scope** (`~/.claude/settings.json`) for
machine-wide protection, or **project scope** (`<project>/.claude/settings.json`) to scope
it to one project (e.g. the app whose `Qualification/` pack you want to protect). Because
the marker is opt-in per file, user scope is safe — it only bites on files you've locked.

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

Replace the path with the absolute path to this repo (keep the quotes — the repo path
contains spaces). **Restart Claude Code** (or run `/hooks`) so it picks up the change.

### Design choice: fail-open vs. fail-closed

This hook **fails open** — if it can't parse the event or read the file, it *allows* the
edit rather than wedge the session. That's the safe default for a learning/utility hook.
For a validated, production deployment protecting real GxP records you would likely flip
it to **fail-closed** (block on any error), so the protection can't be defeated by making
the hook crash. One-line change in the script.

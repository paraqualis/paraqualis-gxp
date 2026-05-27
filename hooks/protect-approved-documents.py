#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""Claude Code PreToolUse hook: refuse edits to approved (locked) documents.

Register this against the file-writing tools (Edit, Write, MultiEdit, NotebookEdit).
A document is "locked" once it contains this marker line anywhere in its text:

    <!-- PARAQUALIS-LOCK: approved -->

When Claude tries to modify a locked file, this hook blocks the tool call and tells
Claude why — so an approved record cannot be changed in place. That is the controlled
way to treat an approved GxP document: to revise it you issue a new version through
change control, you don't quietly overwrite the approved one.

How it works: Claude Code sends the pending tool call as JSON on stdin. We read the
target file path, check the file on disk for the marker, and:
  * exit 2  -> BLOCK the call (whatever we print to stderr is shown to Claude as the reason)
  * exit 0  -> ALLOW the call
A file that doesn't exist yet (a new file being created) is always allowed.
"""
import json
import sys

LOCK_MARKER = "<!-- PARAQUALIS-LOCK: approved -->"


def main() -> int:
    # Read the event Claude Code hands us. If we can't parse it, fail OPEN (allow)
    # rather than wedge the whole session on a malformed payload.
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = event.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return 0  # not a file-writing call we recognise — nothing to protect

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except FileNotFoundError:
        return 0  # creating a brand-new file — allow
    except Exception:
        return 0  # can't read it — fail open

    if LOCK_MARKER in content:
        sys.stderr.write(
            f"Blocked: {path} is an APPROVED, locked document (it contains the marker "
            f"'{LOCK_MARKER}'). Approved records must not be edited in place. To revise "
            f"it, create a new version under change control; the lock marker should only "
            f"be removed by appropriately qualified and authorized personnel."
        )
        return 2  # exit 2 -> Claude Code blocks the tool and shows the reason above

    return 0  # not locked — allow the edit


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE.
"""
SessionStart hook: show a one-time "say hello" note the first time the plugin runs.

The only way ParaQualis learns who uses the toolkit is if people tell us — the plugin has
no telemetry and never will (see PRIVACY.md). So the first session after install shows a
short invitation to get in touch, then records that it has done so and stays silent.

State: a single marker file, `welcome-shown`, in the plugin's persistent data directory
(`${CLAUDE_PLUGIN_DATA}`, provided by Claude Code). Local only; nothing leaves the machine.
Delete the marker to see the note again.
"""
import json
import os
import sys
from datetime import datetime, timezone

MESSAGE = (
    "Thanks for installing ParaQualis GxP. We're a small team and would genuinely like to "
    "know who is using it and what for. Drop us a line at hello@paraqualis.com, or say hello "
    "at https://github.com/paraqualis/paraqualis-gxp/discussions. "
    "(This note appears once.)"
)


def main() -> int:
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if not data_dir:
        # Fail loud: without the data dir we cannot remember we've shown the note, and
        # showing it every session would be worse than not showing it at all.
        print("paraqualis-gxp welcome-once: CLAUDE_PLUGIN_DATA is not set — this Claude Code "
              "version does not provide a plugin data directory; welcome note skipped. "
              "Update Claude Code to clear this message.", file=sys.stderr)
        return 1

    marker = os.path.join(data_dir, "welcome-shown")
    if os.path.exists(marker):
        return 0

    os.makedirs(data_dir, exist_ok=True)
    with open(marker, "w") as f:
        f.write(datetime.now(timezone.utc).isoformat() + "\n")

    print(json.dumps({"systemMessage": MESSAGE}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

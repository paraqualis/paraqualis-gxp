#!/usr/bin/env bash
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE.
#
# Installs this repo's Claude Code slash commands by symlinking each command
# family under commands/ into ~/.claude/commands/. Idempotent and safe to
# re-run. Run this once on any machine after cloning the repo.
#
#   ./install.sh

set -euo pipefail

# Resolve the directory this script lives in (the repo root), even if invoked
# from elsewhere or via a relative path.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_DIR/commands"
DEST="${CLAUDE_HOME:-$HOME/.claude}/commands"

mkdir -p "$DEST"

echo "Linking command families from:"
echo "  $SRC"
echo "into:"
echo "  $DEST"
echo

# Prune symlinks we previously created that now dangle — e.g. a command or
# family renamed/removed in the repo. Only touch links pointing back into THIS
# repo, and only if their target no longer exists; never disturb the user's own.
for link in "$DEST"/*; do
  [ -L "$link" ] || continue
  case "$(readlink "$link")" in
    "$REPO_DIR"/*)
      if [ ! -e "$link" ]; then
        rm -f "$link"
        echo "  pruned   $(basename "$link") (target gone)"
      fi
      ;;
  esac
done

for entry in "$SRC"/*; do
  [ -e "$entry" ] || continue            # skip if commands/ is empty
  name="$(basename "$entry")"
  target="$DEST/$name"

  if [ -L "$target" ]; then
    # Existing symlink — repoint it (handles repo moves).
    ln -sfn "$entry" "$target"
    echo "  updated  $name -> $entry"
  elif [ -e "$target" ]; then
    # A real file/dir is in the way — don't clobber the user's own commands.
    echo "  SKIPPED  $name (a non-symlink already exists at $target)"
  else
    ln -s "$entry" "$target"
    echo "  linked   $name -> $entry"
  fi
done

echo
echo "Done. Restart Claude Code so it picks up the new commands."

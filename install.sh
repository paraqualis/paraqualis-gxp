#!/usr/bin/env bash
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE.
#
# Installs this repo's Claude Code assets by symlinking each command family under
# commands/ into ~/.claude/commands/ and each skill under skills/ into
# ~/.claude/skills/. Idempotent and safe to re-run. Run once on any machine after
# cloning the repo.
#
#   ./install.sh

set -euo pipefail

# Resolve the directory this script lives in (the repo root), even if invoked
# from elsewhere or via a relative path.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"

# link_tree <source-dir> <dest-dir> <label>
# Symlinks each entry in source-dir into dest-dir, pruning our own stale links.
link_tree() {
  local SRC="$1" DEST="$2" LABEL="$3"
  [ -d "$SRC" ] || return 0               # nothing of this kind in the repo

  mkdir -p "$DEST"
  echo "Linking $LABEL from $SRC into $DEST"

  # Prune symlinks we previously created that now dangle (renamed/removed in repo).
  # Only touch links pointing back into THIS repo whose target no longer exists.
  for link in "$DEST"/*; do
    [ -L "$link" ] || continue
    case "$(readlink "$link")" in
      "$REPO_DIR"/*)
        if [ ! -e "$link" ]; then
          rm -f "$link"; echo "  pruned   $(basename "$link") (target gone)"
        fi ;;
    esac
  done

  for entry in "$SRC"/*; do
    [ -e "$entry" ] || continue
    local name target; name="$(basename "$entry")"; target="$DEST/$name"
    if [ -L "$target" ]; then
      ln -sfn "$entry" "$target"; echo "  updated  $name"
    elif [ -e "$target" ]; then
      echo "  SKIPPED  $name (a non-symlink already exists at $target)"
    else
      ln -s "$entry" "$target"; echo "  linked   $name"
    fi
  done
  echo
}

link_tree "$REPO_DIR/commands" "$CLAUDE_DIR/commands" "command families"
link_tree "$REPO_DIR/skills"   "$CLAUDE_DIR/skills"   "skills"
link_tree "$REPO_DIR/agents"   "$CLAUDE_DIR/agents"   "subagents"

# If run inside the source repo, enable the tracked git hook that keeps docs/OVERVIEW.md's
# catalog in sync on every commit. Harmless elsewhere.
if [ -d "$REPO_DIR/.git" ] && [ -d "$REPO_DIR/.githooks" ]; then
  git -C "$REPO_DIR" config core.hooksPath .githooks 2>/dev/null \
    && echo "git hooks: core.hooksPath -> .githooks (auto-refreshes the docs catalog)"
fi

echo "Done. Restart Claude Code so it picks up the new commands, skills, and agents."

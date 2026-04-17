#!/usr/bin/env bash
# Merge origin/main into the current branch after an automated data commit, then push.
# If the merge conflicts on catalog / ledger / library files, resolve via union merge script.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git fetch origin main

if git merge FETCH_HEAD -m "merge origin/main before push [automated]"; then
  git push
else
  python scripts/merge_data_snapshot_conflicts.py
  git add CONTENT_LIBRARY.md content_catalog.json data/generations.json || true
  if git diff --staged --quiet; then
    echo "❌ Merge conflict resolution produced no staged changes." >&2
    exit 1
  fi
  git commit -m "merge origin/main (resolve data files) [automated]"
  git push
fi

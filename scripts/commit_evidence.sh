#!/usr/bin/env bash
# Commit evidence produced by THIS workflow run without ever rebasing it onto someone else's evidence.
#
#   scripts/commit_evidence.sh "<commit message>" <path> [<path> ...]
#
# The listed paths are owned wholesale by the calling run (its report files), so on a race we do not merge: we snapshot
# the paths, reset the checkout to origin/main, put the snapshot back, commit and push; repeat with backoff if the push is
# rejected. `git pull --rebase` cannot merge wholesale-replaced result files and left eval run 40012594419's evidence
# unpublished (DECISIONS.md 2026-10-23). Exit 0 when there is nothing to commit, non-zero if the push never lands.
set -euo pipefail
msg="$1"; shift
[ "$#" -ge 1 ] || { echo "usage: $0 <message> <path>..." >&2; exit 2; }
git config user.name civiclens-bot
git config user.email actions@users.noreply.github.com
tmp=$(mktemp -d)
for p in "$@"; do
  if [ -e "$p" ]; then mkdir -p "$tmp/$(dirname "$p")"; cp -a "$p" "$tmp/$p"; fi
done
for attempt in 1 2 3 4 5; do
  git fetch -q origin main
  git reset -q --hard origin/main
  for p in "$@"; do
    if [ -e "$tmp/$p" ]; then rm -rf "$p"; mkdir -p "$(dirname "$p")"; cp -a "$tmp/$p" "$p"; fi
  done
  git add -A -- "$@" 2>/dev/null || true
  if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
  git commit -q -m "$msg"
  if git push -q origin HEAD:main; then echo "pushed $(git rev-parse --short HEAD)"; exit 0; fi
  echo "push rejected (attempt $attempt); retrying on top of the new origin/main"
  sleep $((10 * attempt))
done
echo "::error::evidence push failed after 5 attempts"; exit 1

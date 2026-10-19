#!/usr/bin/env bash
set -euo pipefail
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required."; exit 1; }
gh auth status >/dev/null

OWNER="$(gh repo view --json owner -q .owner.login)"

echo "GitHub Projects may require: gh auth refresh -s project"
EXISTING="$(gh project list --owner "$OWNER" --format json --jq '.projects[] | select(.title=="Telegraph Bounties") | .number' 2>/dev/null || true)"
if [[ -n "$EXISTING" ]]; then
  NUM="$EXISTING"
  echo "Using existing project #$NUM"
else
  NUM="$(gh project create --owner "$OWNER" --title "Telegraph Bounties" --format json --jq '.number')"
fi

echo "Project #$NUM ready. Open with: gh project view $NUM --owner $OWNER --web"
echo "Recommended views: P0, By Work Type, By Status, H2 Missions."
echo "Keep Issues as contributor-facing source of truth; use the Project as maintainer control plane."

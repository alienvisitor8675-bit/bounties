#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-}"
NAME="${2:-telegraph-bounties}"
if [[ -z "$OWNER" ]]; then
  echo "Usage: ./scripts/publish_repo.sh <github-org-or-owner> [repo-name]"
  exit 2
fi
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required."; exit 1; }
gh auth status >/dev/null

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
make prepush

BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "main" ]]; then
  echo "Expected local branch 'main', got '$BRANCH'."
  exit 1
fi

if gh repo view "$OWNER/$NAME" >/dev/null 2>&1; then
  echo "$OWNER/$NAME already exists. Not creating or overwriting it."
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/$OWNER/$NAME.git"
  fi
  git push -u origin main
else
  gh repo create "$OWNER/$NAME" --public --source=. --remote=origin --push \
    --description "Open bounties for machine intelligence: Miners, Evaluators, Apps, tooling and network hardening." \
    --homepage "https://hackathon.telegraphprotocol.com/"
fi

make bootstrap

echo
echo "Repository pushed and bootstrapped."
echo "Before ANNOUNCING it publicly: approve real launch bounties, run make seed-h2, then make launch-check."

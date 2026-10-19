#!/usr/bin/env bash
set -euo pipefail

command -v gh >/dev/null || { echo "GitHub CLI (gh) is required: https://cli.github.com/"; exit 1; }
gh auth status >/dev/null
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

echo "Configuring $REPO"

gh repo edit "$REPO" \
  --enable-issues \
  --enable-discussions \
  --enable-projects \
  --enable-wiki=false \
  --description "Permanent demand-driven intelligence opportunities: Providers, Evaluators, Apps, integrations and tooling." \
  --homepage "https://telegraphprotocol.com/" \
  --add-topic ai \
  --add-topic agents \
  --add-topic machine-intelligence \
  --add-topic bounties \
  --add-topic developer-tools \
  --add-topic web3 \
  --add-topic hackathon

create_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --repo "$REPO" --color "$color" --description "$desc" --force >/dev/null
}

# Work type
create_label "opportunity:provider" "006B75" "Commercial Provider recruitment; not a claimable code bounty"

create_label "work:miner" "1D76DB" "Miner / intelligence-supply work"
create_label "work:evaluator" "8250DF" "Evaluation and ranking-measurement work"
create_label "work:app" "0E8A16" "Apps, Agents and integrations"
create_label "work:protocol" "5319E7" "Protocol implementation / reliability"
create_label "work:tooling" "006B75" "SDK, developer tooling, docs or observability"
create_label "work:security" "B60205" "Public security hardening work"

# Gap type
create_label "gap:supply" "54AEFF" "Missing or weak intelligence supply"
create_label "gap:evaluation" "C5DEF5" "Missing or weak evaluation"
create_label "gap:integration" "BFDADC" "Application / integration blocker"
create_label "gap:quality" "FBCA04" "Quality / usefulness gap"
create_label "gap:latency" "FEF2C0" "Latency or throughput gap"
create_label "gap:coverage" "D4C5F9" "Geographic, domain, data or scenario coverage gap"
create_label "gap:reliability" "F9D0C4" "Availability / reliability gap"
create_label "gap:tooling" "C2E0C6" "Developer tooling / DX gap"
create_label "gap:security" "B60205" "Public hardening gap"

# Priority
create_label "priority:p0" "B60205" "Blocks important demand or a critical time-sensitive market outcome; fix first"
create_label "priority:p1" "D93F0B" "Materially improves readiness or usefulness"
create_label "priority:p2" "FBCA04" "Useful; not currently blocking important demand"

# Status
create_label "status:triage" "D4C5F9" "Needs maintainer normalization and acceptance criteria"
create_label "status:open" "0E8A16" "Ready to be picked up"
create_label "status:claimed" "1D76DB" "A contributor is actively working on it"
create_label "status:review" "8250DF" "Submission awaiting verification"
create_label "status:blocked" "B60205" "Blocked on another dependency"
create_label "status:done" "2EA44F" "Verified complete"

# Source
create_label "source:h2" "0052CC" "Demand exposed by Telegraph Hackathon Season II"
create_label "source:mainnet" "0B3D91" "Verified gap exposed by live network usage"
create_label "source:customer" "006B75" "Approved, sanitized demand from a customer / integration; not necessarily a paid order"
create_label "source:roadmap" "5319E7" "Telegraph roadmap work"
create_label "source:security" "B60205" "Security-driven hardening"
create_label "source:protocol" "0E8A16" "Publicly evidenced evaluation needs from an authorized protocol/Explorer state export"
create_label "source:release" "A371F7" "Gap exposed by an important external AI/model/API/tool release"

# Discovery / reward
create_label "good first bounty" "7057FF" "Small, clear, newcomer-friendly task"
create_label "help wanted" "008672" "External contribution wanted"
create_label "reward:funded" "2EA44F" "Reward terms are explicitly funded on the Issue"
create_label "reward:unfunded" "C5DEF5" "No monetary/token reward is currently committed"
create_label "reward:paid" "0E8A16" "Reward payout completed"

# H2 missions
for mission in exchange stablecoin institutional-markets legal conflict-intelligence resources-agriculture consumer-platform commodities personal-agent model-economy autonomous-systems mining-power asset-management web3-defi consumer-automation; do
  create_label "mission:$mission" "EDEDED" "Season II mission: $mission"
done

echo "Done."
echo "Next: triage public-safe ongoing work via Issue Forms; use make seed-h2 only for approved Season II seed items."
echo "Manual launch step: upload assets/social-preview.png as the GitHub social preview."

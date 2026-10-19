# Evaluation contributions: private diagnostics → minimal public opportunities

This repository coordinates **public Category-level evaluation contributions** around Telegraph V2. It is **not** a second oracle, ranking protocol, consensus layer, funding mechanism, or a public dashboard of weak Intents. Existing V2 evaluator competition, hidden qualification, background Miner ranking, and Validator finality remain unchanged.

## Security model: minimum necessary disclosure

**Private by default:** Raw node/Explorer Intent observations, per-Intent missing coverage and quality diagnostics, source concentration, exact counter values, source freshness distribution, alert flags, adapter/profile failure reasons, internal reference URLs, demand/blocker telemetry linked to specific vulnerabilities, hidden qualification material and test selection logic.

**Public after projection and manual approval:** Only a broadly published Category name, a generic request for compatible evaluation methods/material, a stable *keyed opaque identifier*, and `triage`/`unfunded` status. The public issue does not distinguish which underlying deficiency triggered it. Multiple internal problems in one Category collapse into **one** broad, review-only public opportunity. This is a deliberate information/actionability tradeoff; more precise scopes require authorized private coordination or safe-to-publish specifications that do not expose exploitable deficits.

An earlier implementation published exact gap types, sampled Intent IDs, URLs, thresholds and source counts. **Do not use that format for public feeds or GitHub Issue creation.** The current publisher rejects it. Previously published detailed GitHub Issues require maintainer review and possible redaction; the new publisher halts if it sees a legacy generated issue. Public issue edits cannot erase forks, notifications or cached copies.

Information already available from V2's public chain or an otherwise public API remains publicly reconstructable. Restricting this repo reduces *additional* attack surface; it does not hide on-chain information. The protocol team must review what is disclosed before storing or emitting it publicly.

## Boundaries

| Component | Responsibility / visibility |
|---|---|
| Node/protocol | V2 source of truth, no bounty logic in Validators |
| Authorized indexer | Secure ingestion of detailed, non-secret per-Intent state, risk/coverage calculations, application blockers and optional verified spending; access control, minimal retention and no public telemetry dumps |
| Internal gap detector (`evaluation_opportunities.py`) | Computes detailed diagnostics **in process**, aggregates on Category/adapter/profile/gap; does not treat accepted labels as true |
| **Public projection** (`evaluation_publication.py`) | Explicit allowlist, one opaque category opportunity, no gaps, thresholds, counts, profile/adapter IDs, Intent IDs, demand, source identifiers or evidence URLs |
| GitHub sync (`sync_evaluation_issues.py`) | Validates the public projection and stable authorization key; requires maintainer approvals and publishes only unfunded triage Issues |
| Maintainers/contributors | Coordinate specific proof privately where sensitive; submit through existing V2 admission and qualification interfaces; only approve bounty rewards when explicitly funded/verified |

## Internal input contract (trusted operator/indexer only)

The existing input format is **unchanged** and is not an authorized public export:

1. `profiles.json`: Category ID, adapter ID, profile ID, public-compatible schema, reference requirements and private operational thresholds (`min_eligible_items`, `min_fresh_items`, `min_source_domains`, `max_material_age_hours`, `min_case_coverage`). These thresholds are **discovery settings**, not V2 consensus constants.
2. `snapshot.ndjson`: Intent ID/profile ID, UTC observation time, `observed` counters (eligible/fresh items, independently assessed upstream-source domains, case coverage, qualified Evaluator presence, adapter availability and quality alert), plus optional verified demand (`qualified_paid_usdc_30d`, `blocked_apps`).

The schema rejects unexpected profile/snapshot fields; **do not send evidence URLs, hidden material or request payloads to this integration at all**. The files in `examples/` contain **fictional fixtures only**, not real mainnet state or thresholds. They demonstrate the internal contract and MUST NOT be copied into public Issues or treated as evidence of current vulnerabilities. Missing required metrics fail closed; do not invent zeros, synthetic source independence, payment activity, or confidence.

For production, ingest raw observations inside a trusted indexer or a protected operator workspace, with access controls, private logging and retention limits. Avoid storing the detailed files in this public Git repository, PR artifacts, GitHub Actions output or public Explorer responses. The prototype reads NDJSON line by line but keeps a set of seen Intent IDs; its actual million-Intent memory/throughput is **not** certified.

## Public output contract

Default CLI output is a strict **v2 public-only** projection; private diagnostics are not emitted by the CLI.

```json
{
  "schema_version": 2,
  "generated_at": "2026-10-11T10:00:00Z",
  "scope": "public category-level review candidates only; no quality/ranking claims or funded reward",
  "opportunities": [
    {
      "id": "evalpub-<opaque-keyed-id>",
      "category_id": "weather-intelligence",
      "work_type": "evaluation-contributions",
      "review_status": "triage",
      "funded_reward": false
    }
  ]
}
```

The placeholder above is not an actual valid ID. The ID is derived from a **stable secret HMAC key and the Category**, not from a guessable gap/profile hash. Unknown fields are rejected at the sync boundary; HTML or Markdown from private feed values is never copied into public Issue content.

## Demo: strictly public output

From the repo root:

```bash
make evaluation-demo
python3 scripts/sync_evaluation_issues.py \
  --opportunities <temp dir>/telegraph-evaluation-opportunities-demo.json \
  --now 2026-10-11T10:00:00Z
```

The demo uses an **ephemeral, discarded secret** and fictitious data; it is NOT suitable for publishing GitHub Issues because the resulting public IDs change on each demo run.

For live workflows, securely provision a high-entropy, **stable** secret (at least 32 characters) as `TELEGRAPH_BOUNTY_PUBLICATION_KEY` in the protected operator environment. For example, generate it once with `python3 -c 'import secrets; print(secrets.token_urlsafe(48))'` and store it in your private secret manager. Never log, echo, commit or rotate casually: rotations change category opportunity IDs and require a controlled reconciliation.

Then with private inputs kept **outside** the public repo:

```bash
python3 scripts/evaluation_opportunities.py \
  --profiles /secure/private-profiles.json \
  --snapshot /secure/private-observations.ndjson \
  --output /tmp/public-evaluation-opportunities.json
./tb needs /tmp/public-evaluation-opportunities.json
```

The output file is public-safe (but production deployment still requires review of the upstream trust boundary). The CLI fails closed if the publication key or required observations are missing. Avoid embedding credentials in CLI arguments or filenames.

## Public GitHub triage publication (never automatic)

Maintainer reviews a public ID and **privately confirms** the need. Approval input stays in a protected workspace:

```json
{
  "approved_ids": ["evalpub-<real-24-hex-id>"],
  "verified_by": "maintainer-github-login"
}
```

```bash
python3 scripts/sync_evaluation_issues.py \
  --opportunities /tmp/public-evaluation-opportunities.json \
  --approvals /secure/verified-approvals.json \
  --repo OWNER/REPO --apply
```

`--apply` requires the stable key in the environment, explicit approved IDs, and an authenticated GitHub CLI. It verifies keyed IDs and refuses private/legacy schema. Issues start as `status:triage`, `reward:unfunded`; no issue is automatically funded, claimed, opened, closed, reopened or paid. The sync never overwrites an existing claimable/claimed Issue. Legacy `evalgap-*` issues are a manual redaction/migration blocker, not silently republished.

**Before `/open`:** maintainers must ensure public acceptance criteria are safe *and* workable without publishing exploitable diagnostic thresholds. Provide private details through a secure contribution/review channel when necessary. Do not promise a funded bounty unless verified under the existing reward-locking workflow. Public Issues may remain broad calls for contributions rather than becoming claimable until an appropriately safe, verifiable scope exists.

## Quality and economics unchanged

- Material must apply to the actual Intent scope, not merely share Category vocabulary. Match valid location/time/language/task parameters where applicable.
- Independently sourced references and evidence are preferable to repackaged labels. Mechanical admission, source counts and random sampling are not correctness proofs.
- Material contributions and Canonical Evaluator promotion still run through V2's authorized commitment/competition/qualification logic. Keep hidden cases hidden where supported by V2.
- Category-level WASM scoring logic can be reused for compatible Intents, but ranking and economic accounting remain per Intent.
- Public opportunities merely coordinate work. Protocol Evaluator emissions remain separate and demand-backed; no bounty or reward is invented from a detected gap.
- For routable-but-unranked Intents, use an explicitly disclosed fallback instead of presenting fallback as a quality ranking.

## Required integration (not included in this repo)

The node team should expose only the minimum needed **to an authorized internal indexer**. That indexer derives any source-diversity/freshness/coverage estimates and passes only the **strict public projection** to GitHub. Do not create a public endpoint serving this internal NDJSON feed. If state is already public on-chain, clearly identify that limitation; this patch cannot make it private.

# Evaluation contribution pipeline

This repository coordinates **public Category-level evaluation contributions** for Telegraph V2. V2 remains authoritative for evaluator competition, qualification, Miner ranking and Validator finality. Funding follows the repository's separate reward process.

## Security model: minimum necessary disclosure

**Private by default:** Raw node/Explorer Intent observations, per-Intent missing coverage and quality diagnostics, source concentration, exact counter values, source freshness distribution, alert flags, adapter/profile failure reasons, internal reference URLs, demand/blocker telemetry linked to specific vulnerabilities, hidden qualification material and test selection logic.

**Public after projection and manual approval:** A broadly published Category name, a general request for compatible evaluation methods or material, a stable *keyed opaque identifier*, and `triage`/`unfunded` status. The public Issue omits the underlying trigger. Multiple internal findings in one Category collapse into **one** broad, review-only opportunity. More precise scopes require authorized private coordination or specifications approved for publication.

The publisher rejects legacy records containing exact gap types, sampled Intent IDs, URLs, thresholds or source counts. If it detects an older generated Issue in that format, it stops for maintainer review and possible redaction. Edits to a public Issue cannot remove copies already present in forks, notifications or caches.

Information available from V2's public chain or another public API remains reconstructable. This repository limits additional disclosure. The protocol team reviews data before storing or emitting it publicly.

## Boundaries

| Component | Responsibility / visibility |
|---|---|
| Node/protocol | V2 source of truth; Validators remain independent of bounty logic |
| Authorized indexer | Secure ingestion of detailed, non-secret per-Intent state, risk and coverage calculations, application blockers and optional verified spending; access control and minimal retention |
| Internal gap detector (`evaluation_opportunities.py`) | Computes detailed diagnostics **in process** and aggregates by Category, adapter, profile and gap; accepted labels still require verification |
| **Public projection** (`evaluation_publication.py`) | Explicit allowlist and one opaque Category opportunity; private fields stay inside the operator boundary |
| GitHub sync (`sync_evaluation_issues.py`) | Validates the public projection and stable authorization key; requires maintainer approvals and publishes only unfunded triage Issues |
| Maintainers/contributors | Coordinate specific proof privately where sensitive; submit through existing V2 admission and qualification interfaces; only approve bounty rewards when explicitly funded/verified |

## Internal input contract (trusted operator/indexer only)

The input format is an internal operator contract rather than an authorized public export:

1. `profiles.json`: Category ID, adapter ID, profile ID, public-compatible schema, reference requirements and private operational thresholds (`min_eligible_items`, `min_fresh_items`, `min_source_domains`, `max_material_age_hours`, `min_case_coverage`). These are discovery settings rather than V2 consensus constants.
2. `snapshot.ndjson`: Intent ID/profile ID, UTC observation time, `observed` counters (eligible/fresh items, independently assessed upstream-source domains, case coverage, qualified Evaluator presence, adapter availability and quality alert), plus optional verified demand (`qualified_paid_usdc_30d`, `blocked_apps`).

The schema rejects unexpected fields. Keep evidence URLs, hidden material and request payloads outside this integration. Files in `examples/` are **fictional fixtures** that demonstrate the contract; they contain no mainnet state or thresholds and provide no evidence about current vulnerabilities. Missing required metrics fail closed. Supply observed values rather than assumed zeros, source independence, payment activity or confidence.

For production, ingest raw observations inside a trusted indexer or protected operator workspace with access controls, private logging and retention limits. Store detailed files outside this public repository, PR artifacts, GitHub Actions output and public Explorer responses. The implementation reads NDJSON line by line and keeps a set of seen Intent IDs; benchmark it against the intended production volume before deployment.

## Public output contract

The CLI emits a strict **v2 public projection** and keeps private diagnostics inside the operator process.

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

The placeholder is illustrative. Real IDs derive from a **stable secret HMAC key and the Category**, making them independent of gap and profile details. The sync boundary rejects unknown fields and constructs Issue content from an allowlist rather than private feed text.

## Demo

From the repo root:

```bash
make evaluation-demo
python3 scripts/sync_evaluation_issues.py \
  --opportunities <temp dir>/telegraph-evaluation-opportunities-demo.json \
  --now 2026-10-11T10:00:00Z
```

The demo uses an ephemeral secret and fictitious data. Its IDs change on every run, so use the stable operator key for live publication.

For live workflows, provision a high-entropy, **stable** secret of at least 32 characters as `TELEGRAPH_BOUNTY_PUBLICATION_KEY` in the protected operator environment. For example, generate it once with `python3 -c 'import secrets; print(secrets.token_urlsafe(48))'` and store it in a private secret manager. Keep it out of logs, shell history, commits and artifacts. A rotation changes Category opportunity IDs and requires controlled reconciliation.

Then with private inputs kept **outside** the public repo:

```bash
python3 scripts/evaluation_opportunities.py \
  --profiles /secure/private-profiles.json \
  --snapshot /secure/private-observations.ndjson \
  --output /tmp/public-evaluation-opportunities.json
./tb needs /tmp/public-evaluation-opportunities.json
```

The output file follows the public schema; production deployment still requires review of the upstream trust boundary. The CLI fails closed when the publication key or required observations are missing. Keep credentials out of CLI arguments and filenames.

## Public GitHub triage publication

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

`--apply` requires the stable key in the environment, explicit approved IDs and an authenticated GitHub CLI. It verifies keyed IDs and rejects private or legacy schemas. New Issues start as `status:triage`, `reward:unfunded`. Funding, claim, status and payout decisions remain manual. The sync preserves existing claimable or claimed Issues. A legacy `evalgap-*` Issue stops publication for manual redaction and migration.

**Before `/open`:** maintainers confirm that public acceptance criteria are useful and safe to publish. Sensitive targets stay in the secure contribution and review channel. Funded bounties also pass the reward authorization workflow. A broad call for contributions can remain in triage until it has a safe, verifiable claim scope.

## Quality and economics unchanged

- Material must apply to the actual Intent scope and match relevant location, time, language and task parameters.
- Prefer independently sourced references and evidence to repackaged labels. Semantic correctness requires reproducible evidence beyond admission checks, source counts and random sampling.
- Material contributions and Canonical Evaluator promotion still run through V2's authorized commitment/competition/qualification logic. Keep hidden cases hidden where supported by V2.
- Category-level WASM scoring logic can be reused for compatible Intents, but ranking and economic accounting remain per Intent.
- Public opportunities coordinate work. Protocol Evaluator emissions remain separate and demand-backed; a detected gap begins as an unfunded triage record.
- For routable-but-unranked Intents, use an explicitly disclosed fallback instead of presenting fallback as a quality ranking.

## Required production integration

The node team should expose the minimum required data **to an authorized internal indexer**. That indexer derives source-diversity, freshness and coverage estimates and passes the **strict public projection** to GitHub. Keep the internal NDJSON feed behind the authorized boundary. Identify any state already public on-chain, since repository filtering cannot make public protocol data private.

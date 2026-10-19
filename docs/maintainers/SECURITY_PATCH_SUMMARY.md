# V2 Bounty Evaluation Discovery: public disclosure hardening

This patch changes **only the evaluation-needs publication boundary**. Original H2 missions, Intents, bounties, reward safeguards, contributor claims, and V2 network/protocol logic are unchanged.

## What is enforced

- Internal detection retains Category/Intent gap analysis but the default generated export is a **strict public v2 projection** containing only `id`, `category_id`, generic `work_type`, `review_status`, `funded_reward` and top-level generation metadata.
- All exact gap types, per-Intent IDs, source counts/concentration, demand and blocker values, compatibility profile IDs, adapter IDs, private URLs, quality alerts, threshold values and internal raw telemetry are **not** included in the exported JSON or auto-generated GitHub issues.
- The public export groups by Category, not gap type or specific Intent; categories with multiple internal gaps produce one general public invitation.
- Public IDs use **HMAC-SHA256** with a private stable operator key (`TELEGRAPH_BOUNTY_PUBLICATION_KEY`), not predictable hashes of exact gap details. Publishing rejects missing/incorrect keys, wrong output schemas, private fields, duplicate identities and stale exports.
- The raw snapshot schema **rejects extra fields** and no longer imports `evidence_url`; this avoids unnecessary ingestion of private links. Input observations must remain in a trusted environment.
- The GitHub publisher still requires explicit maintainer approvals and creates only **unfunded triage issues**. It refuses to act when legacy `evalgap-*` issues with the previous detailed format are detected; maintainers must review/redact those by hand.
- Public Issue templates explicitly prohibit detailed ranking weaknesses and send sensitive details to `SECURITY.md`.
- The public `./tb needs` command accepts **only** the sanitized v2 format and cannot print private diagnostics.
- Unit and mock-transport security regression tests verify the absence of injected canaries in public exports and generated GitHub Issue content.

## Operator handoff

1. Nodes export only necessary existing state to an **authorized indexer**, not an unauthenticated raw-telemetry endpoint. Do not place hidden qualification contents, credentials or user requests in the indexer feeds.
2. Keep raw profiles/snapshots and publisher key outside GitHub and public CI artifacts; use protected storage and a **stable high-entropy** publisher key.
3. Run `scripts/evaluation_opportunities.py` in that environment and publish its **public-safe output only**. Execute `sync_evaluation_issues.py --apply` solely after explicit approval and security review.
4. Confirm that acceptance criteria for a claimable bounty can be safely made public; keep sensitive verification detail in an authorized channel. Existing issues posted prior to hardening require manual review.
5. Remember that **public on-chain data cannot be rendered confidential by an Explorer/indexer filter**. Minimize sensitive public-chain metadata at the protocol design boundary where possible.

## Verification and remaining boundaries

- `python3 scripts/prepush.py` and `make evaluation-demo` passed locally, including original workflows and new adversarial tests.
- No live node or Explorer exporter was connected; no actual GitHub issues were created; no penetration test of deployed components was performed.
- This patch reduces **extra discovery-side information disclosure**. It does not mathematically guarantee evaluation quality, prevent adversarial observations of public chain state, or secure an unreviewed live node/Explorer implementation.

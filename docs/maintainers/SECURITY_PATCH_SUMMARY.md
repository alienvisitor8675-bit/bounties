# Evaluation publication security

The evaluation-needs pipeline separates private diagnostic data from the Category-level opportunities approved for public release. H2 missions, Intents, bounties, reward controls, contributor claims and V2 protocol logic continue through their existing systems.

## Enforced boundary

- Internal detection retains Category and Intent analysis. The generated export is a **strict public v2 projection** containing `id`, `category_id`, generic `work_type`, `review_status`, `funded_reward` and top-level generation metadata.
- Exact gap types, Intent IDs, source counts and concentration, demand and blocker values, compatibility profile IDs, adapter IDs, private URLs, quality alerts, thresholds and raw telemetry stay inside the operator boundary.
- The export groups by Category. Multiple findings in one Category produce one general public invitation.
- Public IDs use **HMAC-SHA256** with a stable private operator key (`TELEGRAPH_BOUNTY_PUBLICATION_KEY`). Publishing rejects missing or incorrect keys, invalid schemas, private fields, duplicate identities and stale exports.
- The raw snapshot schema rejects extra fields and excludes `evidence_url`, keeping private links out of the pipeline. Operators retain observations in a trusted environment.
- The GitHub publisher requires explicit maintainer approval and creates **unfunded triage Issues**. Detection of a legacy `evalgap-*` Issue stops publication for manual review and redaction.
- Public Issue templates route sensitive ranking and evaluation details to `SECURITY.md`.
- The public `./tb needs` command accepts the sanitized v2 format and prints only public fields.
- Unit and mock-transport regression tests place canaries in private inputs and verify that public exports and generated Issue bodies exclude them.

## Operator handoff

1. Nodes export the required state to an **authorized indexer**. Hidden qualification content, credentials and user requests remain in their source systems.
2. Store raw profiles, snapshots and the publisher key outside GitHub and public CI artifacts. Use protected storage and a **stable high-entropy** key.
3. Run `scripts/evaluation_opportunities.py` in that environment and publish its strict public projection. Execute `sync_evaluation_issues.py --apply` after explicit approval and security review.
4. Confirm that acceptance criteria for a claimable bounty can be safely made public; keep sensitive verification detail in an authorized channel. Existing issues posted prior to hardening require manual review.
5. Treat public on-chain data as publicly reconstructable. Minimize sensitive public-chain metadata at the protocol design boundary where possible.

## Verification and scope

- `python3 scripts/prepush.py` and `make evaluation-demo` exercise the workflow and adversarial publication tests locally.
- Deployment validation must cover the live node or Explorer exporter, GitHub publication path and the deployed components' security controls.
- The boundary reduces additional disclosure from the discovery pipeline. Evaluation quality, observations of public-chain state and live infrastructure security require their own controls and review.

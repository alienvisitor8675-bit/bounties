# Funded bounty launch gate

This operator checklist governs the path to funded bounties. Keep funded launch
disabled until responsible humans verify every control. Transfers, protocol changes
and private job execution each require authorization in their own systems.

## Repository deployment

- Independently review workflow changes and verify all seven required checks on
  deployed `main`, in addition to the local test pass.
- The configured code owners are `1xAhmed` and repository owner `telegraphprotocol`.
  Confirm that different trusted humans control the reviewing and submitting
  accounts. Independent review requires a different trusted person. Keep the PR
  pending when an eligible reviewer is unavailable.
- An admin imports both `.github/security/*-ruleset.json` files in Settings → Rules
  → Rulesets → New ruleset → Import a ruleset. Review existing rules first. Enable
  code-owner enforcement when the independent reviewer is available. The main
  ruleset permits no bypass; `v*` tags are restricted to repository administrators.
- Confirm that unreviewed PRs and failed checks block merging. Test force-push and
  release restrictions in a disposable repository/designated test branch.
- Complete [REPO_SETTINGS.md](REPO_SETTINGS.md): account security, least-privilege
  accounts, Actions restrictions, secret scanning, push protection, private reports
  and account recovery. Apply the server settings through GitHub administration.

## Funding and treasury

- Finance names funding approvers, work reviewers, treasury signers and an incident
  owner. Require independent work review and separate payment approval. Choose
  custody/threshold signing appropriate to the actual chain; test recovery.
- Keep keys and recovery material outside GitHub, Actions and contributor machines.
- Maintain an access-controlled ledger containing stable repository/issue and
  claimant IDs, funding authorization, approved reward version/hash, accepted
  evidence/commit, independent reviewer, recipient verification and payout status.
- Record exact network, asset identifier and base-unit amount, plus any approved
  conversion rule. A token symbol, issue edit or `reward:funded` label is insufficient.
- Verify wallet ownership through an authenticated process bound to claimant,
  bounty and network. Use expiry and replay prevention for signed challenges.
  Re-verify address changes independently through the authenticated process.
- Enforce one award per issue and a unique payout ID. Reserve approved funds,
  reconcile pending transactions before retrying and record transaction confirmation
  and appropriate finality. Preserve paid status across reopening and reclaiming.
- Approve per-bounty and aggregate limits before a small, manually reviewed pilot.
  Record all amounts and funding explicitly. Review any future automation as a separate design.
- Compare the claim snapshot with independent funding authorization before every
  payout. The funding ledger and treasury approval authorize payment.

## Operations and recovery

- Run contributor code in disposable environments isolated from production credentials,
  wallets, customer data and hidden evaluation material. Privileged issue-comment jobs
  execute only reviewed repository code.
- Keep private evaluation observations in their authorized environment and publish
  the documented Category-level projection. V2 qualification determines Evaluator status.
- Commands and stale processing share one repository-wide Actions group. GitHub's
  `queue: max` holds at most 100 pending jobs. Monitor overflow/cancellation and
  rerun original jobs. A bot receipt confirms command acceptance. Define separate
  capacity and ordering controls if the service requires higher throughput.
- Accepted bot transitions precede label changes. Rerun the original job after an
  ambiguous failure. Scheduled reconciliation repairs open issues. Closed issues
  and edited or deleted receipts need authorized review. GitHub comments are mutable;
  use the access-controlled funding ledger for financial authorization.
- Monitor failed/canceled jobs, role/ruleset changes and funding discrepancies.
  Assign private security reports to a responsible human with response coverage.
- Rehearse pausing workflows/payouts, revoking access, restoring verified state,
  notifying affected participants and independently approving resumption. Rotate
  exposed credentials directly; history rewriting alone leaves them valid.
- Obtain independent review of deployed workflows and the actual payout process
  before increasing financial exposure. Keep sensitive findings private until fixed.

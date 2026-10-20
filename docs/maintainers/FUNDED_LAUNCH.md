# Funded bounty launch gate

This is an operator checklist, not an implemented payment system. Funded launch
remains blocked until responsible humans verify these controls. GitHub approval
never authorizes a transfer, protocol state change or resumption of a private job.

## Repository deployment

- Independently review the workflow changes and verify all seven required checks
  on deployed `main`. A local test pass does not establish deployed protection.
- The configured code owners are `1xAhmed` and repository owner `telegraphprotocol`.
  Confirm that different trusted humans control the reviewing and submitting
  accounts. Two logins controlled by the same person do not provide independent
  review. The author cannot approve their own PR; do not silently bypass review.
- An admin imports both `.github/security/*-ruleset.json` files in Settings → Rules
  → Rulesets → New ruleset → Import a ruleset. Review existing rules first. Do not
  enforce code-owner review until the independent reviewer is available. The main
  ruleset has no bypass; `v*` tags are restricted to repository administrators.
- Confirm that unreviewed PRs and failed checks block merging. Test force-push and
  release restrictions in a disposable repository/designated test branch.
- Complete [REPO_SETTINGS.md](REPO_SETTINGS.md): account security, least-privilege
  accounts, Actions restrictions, secret scanning, push protection, private reports
  and account recovery. Configuration files do not enable server settings.

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
  Re-verify address changes independently; never accept a replacement from a DM alone.
- Enforce one award per issue and a unique payout ID. Reserve approved funds,
  reconcile pending transactions before retrying and record transaction confirmation
  and appropriate finality. Reopening/reclaiming cannot reset a paid award.
- Approve per-bounty and aggregate limits before a small, manually reviewed pilot.
  No amounts or funding are implied here. Automation needs a separately reviewed design.
- Compare the claim snapshot with independent funding authorization before every
  payout. A bot hash cannot establish funding; `/approve` and issue closure cannot pay.

## Operations and recovery

- Run contributor code in disposable environments without production credentials,
  wallets, customer data or hidden evaluation material. Never run contributor code
  inside privileged issue-comment jobs.
- Keep private evaluation observations in their authorized environment; publish
  only the documented Category-level projection. GitHub cannot qualify an Evaluator.
- Commands and stale processing share one repository-wide Actions group. GitHub's
  `queue: max` holds at most 100 pending jobs. Monitor overflow/cancellation and
  rerun original jobs. A command is accepted only after its bot receipt; this is
  not a high-throughput service SLA or strict first-comment-wins guarantee.
- Accepted bot transitions precede label changes. Rerun the original job after an
  ambiguous failure. Scheduled reconciliation repairs open issues. Closed issues
  and edited/deleted receipts need authorized review. GitHub comments remain
  mutable and are not a tamper-proof financial ledger.
- Monitor failed/canceled jobs, role/ruleset changes and funding discrepancies.
  Assign private security reports to a responsible human with response coverage.
- Rehearse pausing workflows/payouts, revoking access, restoring verified state,
  notifying affected participants and independently approving resumption. Rotate
  exposed credentials; rewriting history does not revoke them.
- Obtain independent review of deployed workflows and the actual payout process
  before increasing financial exposure. Keep sensitive findings private until fixed.

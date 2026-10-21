# Maintaining the bounty board

## One rule

Every public bounty should answer five questions in under one minute:

1. **What real outcome is blocked/improvable, or what verified time-sensitive market coverage is missing?**
2. **Which reusable Intent/component causes it?**
3. **What exactly needs to change?**
4. **How will completion be verified?**
5. **How important is it right now?**

If any answer is unclear, keep the Issue in `status:triage`. A commercial Provider opportunity may be an open **recruitment listing** and follows the separate onboarding path.

## Triage: reduce to the reusable primitive

Bad:

> Build an Agriculture Miner.

Good:

> Add independent Miner supply for `WEATHER_FORECAST_VERIFY`; currently blocks multiple active Apps.

Bad:

> Improve evaluation.

Safer public evaluation example:

> Propose a reusable, independently verifiable evaluation methodology for an approved task Category; acceptance details and any non-public coverage weaknesses are reviewed privately.

Keep vulnerable Intent details, private cases, hidden reference answers and known weak implementations in the authorized review channel. Public acceptance criteria must remain reproducible without revealing secret qualification inputs.

## Opening a bounty

New Issue Forms start in `status:triage`.

A maintainer uses `/open` only after:

- the gap is real (for release coverage, verify the canonical release source and the concrete missing market capability);
- it is distinct from existing open and closed Issues;
- the scope is reusable;
- acceptance criteria are objective enough to verify;
- reward terms are clear if funded.

This review is the quality gate for the public board.

## Priority

### P0
Blocks material demand, several Apps, critical reliability or security, or an important time-sensitive market outcome. Major-release coverage may qualify when it is materially relevant to a live Telegraph market; use lower priorities for narrower impact.

### P1
Materially improves quality, coverage, evaluation, integration or developer velocity.

### P2
Useful but not currently blocking important demand.

## Major AI release triage

Use `source:release` only for an externally verifiable model/API/agent/tool/dataset release or material version change.

Before `/open`:

- map the release to existing Intent(s) first;
- verify that access and integration respect provider controls and terms;
- identify the actual missing piece: supply/integration, evaluation, tooling, capacity/reliability, or Intent review;
- make acceptance criteria prove **fair eligibility for normal measurement**;
- apply the same scoring rules used for other eligible Providers;
- publish customer names, commitments, budgets and internal pipeline details only with disclosure approval.

For time-sensitive work, the internal team may complete the gap and submit the same reproducible proof through the public workflow.

See [RELEASE_COVERAGE.md](RELEASE_COVERAGE.md).

## Evaluation-needs triage and Category-level reuse

The protocol or Explorer team should provide current per-Intent counters and Category evaluation requirement profiles to the authorized operator pipeline. The [evaluation needs interface](EVALUATION_NEEDS.md) converts them into grouped **triage candidates**, avoiding one bounty per narrow parameter while leaving V2 unchanged.

Before `/open`, confirm the affected Intents, compatibility of the shared adapter, evidence provenance, freshness, representative test distribution, independent source control, blocked Apps or qualified paid demand where claimed, and a measurement method that applies fairly to every Provider. Schema validation establishes format; semantic claims still need evidence.

GitHub sync requires an explicit local approval list and `--apply` from an authenticated maintainer. It creates triage Issues and preserves existing Issue bodies, rewards, claims and approvals. Closed or absent opportunities require manual review. Awards and protocol state remain outside the sync, and profile thresholds remain discovery policy rather than consensus rules.

## Claims

Accepted bot control comments are the coordination journal; labels are its derived
view. Manual label edits cannot override an existing transition. Use maintainer
commands and rerun the original workflow after an API failure. Scheduled
reconciliation repairs open Issues. Preserve command receipts. All mutating
workflows must retain the shared `bounty-state` concurrency group.

- `/claim` starts one exclusive claim for that Issue. The workflow intentionally supports one claimant/award per Issue.
- `/progress ...` resets the stale-claim timer.
- A warning is posted after 48 hours without progress.
- The claim is released after 72 hours without progress.
- Maintainers can release stale/invalid claims.

For supply or evaluation bounties needing N independent implementations, create separate slot Issues (for example `1/3`, `2/3`, `3/3`), each with one active claim.

## Review

`/approve` requires a recorded submission and a maintainer other than the claimant
and submitter. Payment requires its own authorization. Follow
[the funded-launch gate](maintainers/FUNDED_LAUNCH.md) before advertising funded work.

Reproduce acceptance criteria directly; use screenshots as supporting evidence.

Verify the real thing:

- endpoint responds;
- Intent registration is correct;
- evaluator runs;
- ranking behavior changes as expected;
- tests pass;
- request / receipt / settlement exists where required;
- App consumes the result;
- stated latency/quality threshold is met;
- vulnerability no longer reproduces.

Then `/approve`.

If verification finds fixable problems, use:

```text
/changes <clear reason>
```

This preserves the claimant, returns the Issue from `status:review` to `status:claimed`, records the requested changes, and restarts the 72-hour progress window.

## Issue quality

Prefer one clear bounty over several overlapping proposals. Create Intents for reusable intelligence primitives, Issues for evidenced gaps, and pull requests for requested repository changes.

## What to publish

A completed bounty should be something worth sharing. Publish the useful result:

**problem / coverage gap → builder → proof → what became possible or measurable**

That is stronger than announcing "we closed issue #42."

## Maintainer command authorization

Maintainer-only commands are authorized from the actor's actual repository permission, not GitHub `author_association`. The actor must have `write`, `maintain`, or `admin` permission.

## Reward changes

When `/claim` succeeds, the bot records a snapshot and hash of the visible `## Reward` section. To change terms, release the claim, edit the Issue, and let the contributor decide whether to claim again. Confirm payout against the separate funding authorization.

## Permanent demand board: beyond H2

H2 starts with 15 missions and remains one source of work rather than a catalogue limit. Use `source:h2` for H2 needs, `source:customer` or `source:mainnet` for verified general demand, and `source:release` for external release coverage. Anjoman requests remain private until their owner permits a sanitized capability description; review them according to [DEMAND_INTAKE.md](DEMAND_INTAKE.md).

A **commercial Provider opportunity** uses `opportunity:provider` and keeps commercial contact and terms outside Issues. The command bot rejects bounty commands for this label, including maintainer submission overrides. Other `work:miner` Issues may remain claimable adapter or implementation bounties. Verify commercial demand before applying a customer or mainnet source label.

For normal bounties, closing an Issue records that its public acceptance test passed. Re-run the original authorized application or job and verify eligibility, availability, evaluation, routing and payment before the product owner notifies the customer or authorizes a retry. Record paid usage separately from Issue counts. Keep raw diagnostic thresholds, private buyer details, evaluation weaknesses and sensitive input samples in their authorized systems.

# Maintaining the bounty board

## One rule

Every public bounty should answer five questions in under one minute:

1. **What real outcome is blocked/improvable, or what verified time-sensitive market coverage is missing?**
2. **Which reusable Intent/component causes it?**
3. **What exactly needs to change?**
4. **How will completion be verified?**
5. **How important is it right now?**

If any answer is unclear, keep the issue in `status:triage`. A commercial Provider opportunity is allowed as an open **recruitment listing**, but never a claimable bounty.

## Triage: reduce to the reusable primitive

Bad:

> Build an Agriculture Miner.

Good:

> Add independent Miner supply for `WEATHER_FORECAST_VERIFY`; currently blocks multiple active Apps.

Bad:

> Improve evaluation.

Safer public evaluation example:

> Propose a reusable, independently verifiable evaluation methodology for an approved task Category; acceptance details and any non-public coverage weaknesses are reviewed privately.

Do not publish the exact Intent that is vulnerable, missing private cases, hidden reference answers or the known weak implementation. A public reviewer cannot demand secret qualification inputs as public Issue acceptance criteria.

## Public reports are not automatically bounties

New Issue Forms start in `status:triage`.

A maintainer uses `/open` only after:

- the gap is real (for release coverage, verify the canonical release source and the concrete missing market capability);
- it is not a duplicate;
- the scope is reusable;
- acceptance criteria are objective enough to verify;
- reward terms are clear if funded.

This is the main anti-slop barrier.

## Priority

### P0
Blocks material demand, several Apps, critical reliability/security, or an important time-sensitive market outcome. Major-release coverage may qualify when the release is materially relevant to a live Telegraph market; not every announcement is P0.

### P1
Materially improves quality, coverage, evaluation, integration or developer velocity.

### P2
Useful but not currently blocking important demand.

## Major AI release triage

Use `source:release` only for an externally verifiable model/API/agent/tool/dataset release or material version change.

Before `/open`:

- map the release to existing Intent(s) first;
- verify access/integration can be done without bypassing controls or violating provider terms;
- identify the actual missing piece: supply/integration, evaluation, tooling, capacity/reliability, or Intent review;
- make acceptance criteria prove **fair eligibility for normal measurement**, not a desired rank;
- never special-case scoring to make the new Provider win;
- never publish private customer names, commitments, budgets or internal pipeline details unless approved for disclosure.

If the work is time-sensitive and no contributor can land it fast enough, the internal team may complete it and submit the same reproducible proof. GitHub is the coordination surface, not a reason to let an important market go stale.

See [RELEASE_COVERAGE.md](RELEASE_COVERAGE.md).

## Evaluation-needs triage and Category-level reuse

The protocol/Explorer team should expose current non-secret per-Intent counters and Category evaluation requirement profiles. The new [evaluation needs interface](EVALUATION_NEEDS.md) converts these into grouped **triage candidates**. This prevents one bounty per hyperspecific parameter and does not change V2.

Before `/open`, confirm the affected Intent(s), genuine compatibility of the shared adapter, evidence provenance, freshness, representative test distribution, independent source control, actual blocked Apps/qualified paid demand where claimed, and that the proposed improvement can be measured without preselecting a winner. A passed dataset schema is not proof of truthful labels.

Any GitHub sync requires an explicit local approval list and runs via `--apply` by an authenticated maintainer. It creates triage Issues only and **never** overwrites an existing Issue's body, rewards, claim or approval. Closed/absent opportunities need manual review; no automated award or consensus mutation. Profile thresholds are discovery policy, not protocol consensus thresholds.

## Claims

- `/claim` starts one exclusive claim for that Issue. The workflow intentionally supports one claimant/award per Issue.
- `/progress ...` resets the stale-claim timer.
- A warning is posted after 48 hours without progress.
- The claim is released after 72 hours without progress.
- Maintainers can release stale/invalid claims.

For supply/evaluation bounties needing N independent implementations, create separate slot Issues (for example `1/3`, `2/3`, `3/3`). Do not run parallel claims on one Issue.

## Review

Do not approve screenshots when the acceptance criteria are reproducible.

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

## Issue inflation

One sharp bounty is better than ten vague ones.

Do not turn:

- every mission into an Intent;
- every app output into a protocol primitive;
- every brainstorm into an Issue;
- every generated PR into maintainer work.

## What to publish

A completed bounty should be something worth sharing. Publish the useful result:

**problem / coverage gap → builder → proof → what became possible or measurable**

That is stronger than announcing "we closed issue #42."

## Maintainer command authorization

Maintainer-only commands are authorized from the actor's actual repository permission, not GitHub `author_association`. The actor must have `write`, `maintain`, or `admin` permission.

## Reward changes

The bot snapshots the visible `## Reward` section when `/claim` succeeds. Those terms are locked for that active claim. If terms must change, release the claim, edit the Issue, and have the contributor claim again.

## Permanent demand board: beyond H2

H2 starts with 15 missions but is **not** a catalogue limit or a prerequisite for posting general approved work. Use `source:h2` only for actual H2 needs. Prefer `source:customer`/`source:mainnet` for verified general demands, `source:release` for external release coverage. A request from Anjoman is private until its owner explicitly permits a sanitized capability description to be used; review according to [DEMAND_INTAKE.md](DEMAND_INTAKE.md).

A **commercial Provider opportunity** is separate from a development bounty: mark `opportunity:provider`, keep commercial contact/terms outside Issues, and never assign a `/claim` or GitHub reward to it. The command bot rejects bounty commands on this label, including maintainer submission overrides. Other `work:miner` Issues may remain normal claimable adapter/implementation bounties. The commercial need must be verified before it is labeled as customer/mainnet demand.

For normal bounties, closing an Issue is evidence that the public acceptance test passed; it is **not** proof of Protocol Intent eligibility, independent supply, completion of an Anjoman customer job, or paid adoption. Re-run the original authorized application/job, check availability/evaluation/routing/payment, and only then allow the product owner to notify and reauthorize a retry. Record real paid usage unlocked separately from issue count. Do not expose raw diagnostic thresholds, private buyer details, evaluation weakness or sensitive input samples to prove importance.

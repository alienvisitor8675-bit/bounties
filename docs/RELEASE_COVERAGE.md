# Major AI release coverage

Telegraph markets should stay useful when machine intelligence changes.

When a significant model, API, agent, tool or dataset launches or materially changes, the relevant Telegraph market may need new supply integration, evaluator coverage, compatibility work or—more rarely—an Intent definition/version review.

This repository is where those concrete gaps can become public bounties.

## What counts as a real release-coverage gap

A release-coverage bounty needs evidence, not hype. It should identify:

1. a real, externally verifiable release;
2. the existing Telegraph Intent(s) where the release can reasonably compete, or a clear reason Intent triage is needed;
3. the specific missing integration, evaluation, tooling, capacity or reliability work;
4. objective acceptance criteria that make the release eligible for fair measurement.

A major release can be time-sensitive even when no private customer is named. The evidence is the release itself plus the concrete market-coverage gap. Do **not** invent customer demand, budget, endorsement or usage to justify a bounty.

## Reuse the existing market first

A new model version is not automatically a new Intent.

If the task is already represented by an existing Intent, integrate the new Provider into that market. Create or revise an Intent only when the task itself is materially different or the existing definition cannot measure it defensibly.

Telegraph does not require one universal Provider output schema at the protocol layer. Provider-native interfaces may differ; app/Anjoman/adapters can normalize outputs where a consuming workflow needs a common shape.

## The bounty closes on fair eligibility, not on winning

The acceptance criteria must never require a Provider to become `#1`, beat an incumbent, or produce a predetermined ranking.

Good acceptance criteria prove things such as:

- the Provider can be called through the approved integration path;
- the release is registered against the correct existing Intent/version;
- reference and hidden evaluation cases execute correctly;
- any required app-facing normalization works without changing Provider-native semantics;
- no Provider-specific scoring exception was introduced;
- the ranking can be reproduced under the same rules as other eligible supply;
- required latency, reliability or capacity thresholds are met where they are part of the market definition.

The measured result may be `#1`, `#7`, unchanged from the previous version, or otherwise unremarkable. The bounty is complete when Telegraph can measure the release fairly—not when the result is dramatic.

## Priority

Use `source:release` for these issues.

A release gap may be `priority:p0` when the release is materially important to a live Telegraph market and the useful measurement window is time-sensitive. Do not mark every model announcement P0. P1/P2 remain appropriate when the market impact is narrower or the work can wait.

Work/gap labels should still describe the actual missing piece:

- Provider supply/integration: `work:miner` + `gap:supply` or `gap:integration`;
- Evaluator work: `work:evaluator` + `gap:evaluation`;
- compatibility/tooling: `work:tooling` + `gap:tooling`;
- reliability/capacity: relevant work label + `gap:reliability` / `gap:latency` / `gap:coverage`.

The repository keeps `work:miner` as the protocol-facing label; public issue copy may say **Provider** when that is clearer.

## Maintainer path

```text
verified important release
        ↓
map to existing Intent(s)
        ↓
identify the concrete coverage gap
        ↓
triage issue + objective acceptance criteria
        ↓
/open → contributor claims → builds → submits proof
        ↓
maintainer verifies fair eligibility
        ↓
/approve
        ↓
Telegraph can run the normal evaluation/ranking path
```

If a time-sensitive, strategically important gap is not picked up quickly enough, maintainers may complete the work internally and use the same `/submit` → verification → `/approve` path. The bounty system is leverage; it must not make the public market stale.

## Public proof after completion

A completed release bounty can become a public market event, but the public claim must match what was actually measured.

Examples:

- "Release X entered `CODE_GENERATION` at #3."
- "Release Y displaced the previous leader on this Intent."
- "The incumbent remained #1 after Release Z entered."
- "A new Evaluator changed the ranking after adding valid coverage for Release X."

Link to the exact market/result where possible. Never turn a completed integration bounty into a fabricated performance claim.

### Historical receipt vs current status

A release event should preserve what was actually measured at that moment. A historical receipt should bind, where available, the exact Provider/release version, Intent/version, Evaluator/version, ranking round or timestamp, and measured result. If the claim says a rank changed, preserve the comparison point as well.

A live/current rank object is different. It should clearly identify itself as current and update or expire when ranking state changes. Never let an old `#1` event receipt silently present itself as the Provider's current rank.

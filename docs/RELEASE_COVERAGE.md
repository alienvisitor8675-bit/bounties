# Major AI release coverage

Telegraph markets should stay useful when machine intelligence changes.

When a significant model, API, agent, tool or dataset launches or materially changes, the relevant Telegraph market may need new supply integration, evaluator coverage, compatibility work or—more rarely—an Intent definition/version review.

This repository is where those concrete gaps can become public bounties.

## What counts as a real release-coverage gap

A release-coverage bounty should identify:

1. a real, externally verifiable release;
2. the existing Telegraph Intent(s) where the release can reasonably compete, or a clear reason Intent triage is needed;
3. the specific missing integration, evaluation, tooling, capacity or reliability work;
4. objective acceptance criteria that make the release eligible for fair measurement.

A major release can be time-sensitive even when no private customer is named. The release and the concrete market-coverage gap provide the evidence; customer demand, budget, endorsement and usage claims require their own verification.

## Reuse the existing market first

A new model version usually competes through an existing Intent.

If the task is already represented by an existing Intent, integrate the new Provider into that market. Create or revise an Intent only when the task itself is materially different or the existing definition cannot measure it defensibly.

Provider-native interfaces may differ. Apps, Anjoman and adapters can normalize outputs when a consuming workflow needs a common shape.

## The bounty closes on fair eligibility

Acceptance criteria should establish that the Provider can be measured fairly under the same rules as other eligible supply.

Good acceptance criteria prove things such as:

- the Provider can be called through the approved integration path;
- the release is registered against the correct existing Intent/version;
- reference and hidden evaluation cases execute correctly;
- any required app-facing normalization works without changing Provider-native semantics;
- scoring uses the standard market rules;
- the ranking can be reproduced under the same rules as other eligible supply;
- required latency, reliability or capacity thresholds are met where they are part of the market definition.

The measured result may be `#1`, `#7` or unchanged from the previous version. The bounty is complete when Telegraph can measure the release fairly.

## Priority

Use `source:release` for these issues.

A release gap may be `priority:p0` when it is materially important to a live Telegraph market and the useful measurement window is time-sensitive. Use P1 or P2 for narrower impact or work that can wait.

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

For a time-sensitive strategic gap, maintainers may complete the work internally and use the same `/submit` → verification → `/approve` path.

## Public proof after completion

A completed release bounty can become a public market event, but the public claim must match what was actually measured.

Examples:

- "Release X entered `CODE_GENERATION` at #3."
- "Release Y displaced the previous leader on this Intent."
- "The incumbent remained #1 after Release Z entered."
- "A new Evaluator changed the ranking after adding valid coverage for Release X."

Link to the exact market or result and state only the performance that was measured.

### Historical receipt vs current status

A release event should preserve what was actually measured at that moment. A historical receipt should bind, where available, the exact Provider/release version, Intent/version, Evaluator/version, ranking round or timestamp, and measured result. If the claim says a rank changed, preserve the comparison point as well.

A live rank object should identify itself as current and update or expire when ranking state changes. Historical receipts retain their original timestamp and measurement context.

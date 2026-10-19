# Reward model

A bounty reward exists only when the Issue explicitly defines it.

Paid bounties spell out the terms up front so contributors know whether an issue is paid, how much it pays, and what completion means.

## Reward fields

A funded bounty should define:

| Field | Meaning |
|---|---|
| `funded` | Whether a reward is actually committed. |
| `amount` | Numeric amount. |
| `denomination` | Unit used to state value, e.g. `USD`. |
| `payout_asset` | Asset actually delivered, e.g. `USDC`, `MACHINA`, or another explicitly stated asset. |
| `conversion_rule` | Required when `denomination` and `payout_asset` differ; defines exactly how the payout amount is calculated. |
| `max_awards` | **Must be `1` for one GitHub Issue.** Use separate slot Issues when several independent implementations are required. |
| `eligibility` | Who may participate. |
| `verification_condition` | What must be reproduced/verified before payout. |
| `payout_window` | When payout is expected after approval. |
| `payout_proof` | Added after payment where appropriate. |

## Claim-time reward lock

When `/claim` succeeds, the Telegraph bot records a SHA-256 hash and a visible snapshot of the Issue's `## Reward` section in the trusted claim comment.

**Those claim-time reward terms are immutable for that active claim.** Editing the Issue later does not silently change what the claimant accepted.

If reward terms genuinely need to change, release the claim, update the Issue, and let the contributor claim again under the new terms. Do not retroactively reduce or alter a live claim's reward terms.

## Cross-denomination payouts

If the stated denomination and payout asset are different, the Issue must include an explicit conversion rule before it is published.

Examples:

- `500 USD`, paid in `USDC` → state the exact USD/USDC convention used at payout.
- `500 USD`, paid in `MACHINA` → state the price source, observation window/time, rounding rule, and any fallback/circuit-breaker behavior required to determine the MACHINA amount.

If the conversion rule is missing, the funded bounty is invalid and repository validation must fail.

This bounty rule does not change Telegraph protocol economics. Consumer activity remains USDC-denominated; a bounty payout asset is only the asset used for that bounty reward.

## No implied token promises

If a bounty is stated as `$500`, that does **not** imply a specific MACHINA amount unless the Issue explicitly states the conversion rule and payout asset.

If future MACHINA-denominated or IOU-style rewards are introduced, their terms must be written on the issue before contributors claim it.

## Multiple independent implementations

The automated workflow deliberately enforces **one claimant and one award per GitHub Issue**.

If the network needs N independent Miners, Evaluators, or implementations, create N clearly related **slot Issues** (for example `1/3`, `2/3`, `3/3`) with their own claim state and reward terms.

This keeps claims race-safe and makes each contributor's acceptance/reward state unambiguous. Do not advertise parallel `max_awards > 1` on a single Issue.

## Payout state

Recommended labels:

- `reward:funded`
- `reward:unfunded`
- `reward:paid`

The `reward:funded` label is not enough by itself; the issue body remains authoritative until a claim is created, after which the bot's claim-time reward snapshot locks the terms for that active claim.

## Evaluation-material opportunity rewards

A Category/Intent evaluation-gap alert is not a funded bounty. Generated issues are `status:triage` and `reward:unfunded` until a maintainer separately approves scope **and explicitly funds** a reward under this document. Protocol V2 demand-backed Evaluator emissions are a distinct mechanism tied to Canonical Evaluator eligibility and qualified external paid Consumer demand, not an automatic payout for submitted material, a GitHub claim or closing an issue.

## Commercial Provider opportunities are not bounty rewards

`opportunity:provider` describes qualified recruitment/onboarding of an already-operating API/model/data service; it is not a one-claim/one-award developer bounty. The GitHub `/claim`, `/submit` and `/approve` lifecycle is disabled for these Issues. Any commercial negotiations, compensation or customer commitments must be explicitly handled and approved outside this public repository. `reward:unfunded` means **no reward is committed**; demand or a proposed MACHINA award does not change that.

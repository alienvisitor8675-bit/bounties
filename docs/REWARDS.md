# Reward model

Each Issue states whether its bounty is funded. A funded reward requires complete terms in the Issue.

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

## Claim-time reward record

When `/claim` succeeds, the Telegraph bot records a SHA-256 hash and visible snapshot of the Issue's `## Reward` section in the claim receipt.

The claim receipt preserves the terms the contributor accepted, independently of later edits to the Issue body. GitHub comments remain mutable, so the receipt is an audit record rather than a tamper-proof ledger or proof of funding. Before payment, compare it with the independently authorized funding and payout records described in [FUNDED_LAUNCH.md](maintainers/FUNDED_LAUNCH.md).

To change reward terms, release the active claim, update the Issue, and let the contributor decide whether to claim again under the new terms. Existing claims retain their recorded terms.

## Cross-denomination payouts

When the stated denomination and payout asset differ, the Issue must include an explicit conversion rule before publication.

Examples:

- `500 USD`, paid in `USDC` → state the exact USD/USDC convention used at payout.
- `500 USD`, paid in `MACHINA` → state the price source, observation window/time, rounding rule, and any fallback/circuit-breaker behavior required to determine the MACHINA amount.

Repository validation rejects a funded bounty with a missing conversion rule.

This bounty rule does not change Telegraph protocol economics. Consumer activity remains USDC-denominated; a bounty payout asset is only the asset used for that bounty reward.

## Token-denominated rewards

A bounty stated as `$500` promises a MACHINA amount only when the Issue also defines MACHINA as the payout asset and provides the conversion rule.

If future MACHINA-denominated or IOU-style rewards are introduced, their terms must be written on the issue before contributors claim it.

## Multiple independent implementations

The automated workflow deliberately enforces **one claimant and one award per GitHub Issue**.

If the network needs N independent Miners, Evaluators, or implementations, create N clearly related **slot Issues** (for example `1/3`, `2/3`, `3/3`) with their own claim state and reward terms.

The bot serializes commands and scheduled releases in a shared Actions queue and
records accepted transitions before updating labels. Retrying the original job
repairs partial updates while replay protection prevents duplicate acceptance of its
source comment. This depends on the deployed workflows using that shared queue;
GitHub API updates are separate operations. Use one slot Issue per award.

## Payout state

Recommended labels:

- `reward:funded`
- `reward:unfunded`
- `reward:paid`

The Issue body is authoritative before a claim. After `/claim`, its receipt records the accepted terms for that active claim; the separate funding ledger remains authoritative for payment authorization.

## Evaluation-material opportunity rewards

A Category/Intent evaluation-gap alert begins as `status:triage` and `reward:unfunded`. Funding requires separate scope approval and complete terms under this document. Protocol V2 demand-backed Evaluator emissions are a distinct mechanism tied to Canonical Evaluator eligibility and qualified external paid Consumer demand; GitHub activity does not create protocol emissions.

## Commercial Provider opportunities

`opportunity:provider` describes recruitment and onboarding for an established API, model or data service. These Issues use a commercial process outside the GitHub `/claim`, `/submit` and `/approve` lifecycle. Handle negotiations, compensation and customer commitments through the authorized commercial process. The `reward:unfunded` label means the Issue carries no bounty payment commitment.

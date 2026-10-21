# Governance

This repository coordinates public contribution work for Telegraph. Protocol state, customer data and payment authority remain in their respective production systems.

## Roles

| Role | Who | What they can do |
|---|---|---|
| Contributor | Anyone | Open gap reports, `/claim` an open bounty, `/progress`, `/submit`, `/release` their own claim |
| Maintainer | GitHub users with `write`, `maintain` or `admin` permission on this repository | `/open`, `/block`, `/unblock`, `/changes`, `/approve`, release any claim |
| Operator | Maintainer who holds the private evaluation inputs and publication key | Run the evaluation-opportunity pipeline and publish its approved public output |

Maintainer commands are authorised by the actor's real repository permission, not by `author_association`. The list of people holding these permissions is the repository's collaborator list.

The approving maintainer must be separate from the claimant and submitter. If no
independent reviewer is available, the submission remains in review. GitHub approval
records technical acceptance; payment requires separate funding and treasury approval
under [the funded-launch controls](docs/maintainers/FUNDED_LAUNCH.md).

## Who decides what

| Decision | Decided by |
|---|---|
| A gap is evidenced, reusable, distinct and safe to publish | Maintainer |
| An Issue becomes claimable (`/open`) | Maintainer |
| A submission meets its acceptance criteria (`/approve`) | Maintainer, after reproducing the result |
| A bounty carries a funded reward | Telegraph leadership, written on the Issue before anyone can claim it |
| A capability is production-ready, an Intent or Provider is eligible, or a ranking changes | Telegraph's protocol and production systems |
| A private customer or Anjoman need is published | The owner of that need, through [DEMAND_INTAKE.md](docs/DEMAND_INTAKE.md) |

## Principles

- **Start with evidence.** Every public Issue begins with real demand, an observed failure or a verified release gap (see [AGENTS.md](AGENTS.md)).
- **State the reward.** New Issues begin as `reward:unfunded`; funded work publishes complete terms before claims open. See [docs/REWARDS.md](docs/REWARDS.md).
- **Verify production separately.** Issue closure records that its acceptance criteria passed. Production systems establish whether the network can serve the capability.
- **Protect confidential material.** Keep private diagnostics, hidden evaluation material and customer data in authorized systems.

## Changing the rules

Changes to claim, reward or disclosure rules ship as a pull request that updates the code, tests and matching documents together. At least one maintainer other than the author reviews it. Existing claims retain the reward terms recorded when they were accepted; changing terms requires releasing and recreating the claim.

## Conduct and security

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md).

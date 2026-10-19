# Governance

This repository is the public coordination surface for Telegraph contribution work. It does not hold protocol state, customer data or payment authority.

## Roles

| Role | Who | What they can do |
|---|---|---|
| Contributor | Anyone | Open gap reports, `/claim` an open bounty, `/progress`, `/submit`, `/release` their own claim |
| Maintainer | GitHub users with `write`, `maintain` or `admin` permission on this repository | `/open`, `/block`, `/unblock`, `/changes`, `/approve`, release any claim |
| Operator | Maintainer who holds the private evaluation inputs and the publication key | Run the evaluation-opportunity pipeline and publish its public-safe output |

Maintainer commands are authorised by the actor's real repository permission, not by `author_association`. The list of people holding these permissions is the repository's collaborator list.

## Who decides what

| Decision | Decided by |
|---|---|
| A gap is real, reusable, not a duplicate, and safe to publish | Maintainer |
| An Issue becomes claimable (`/open`) | Maintainer |
| A submission meets its acceptance criteria (`/approve`) | Maintainer, after reproducing the result |
| A bounty carries a funded reward | Telegraph leadership, written on the Issue before anyone can claim it |
| A capability is production-ready, an Intent or Provider is eligible, or a ranking changes | The Telegraph protocol and production systems, never GitHub |
| A private customer or Anjoman need is published | The owner of that need, through [DEMAND_INTAKE.md](docs/DEMAND_INTAKE.md) |

## Principles

- **Gaps, not tasks for their own sake.** Every public Issue starts from real demand, an observed failure or a verified release gap (see [AGENTS.md](AGENTS.md)).
- **No reward unless the Issue defines it.** Today new Issues are `reward:unfunded`. See [docs/REWARDS.md](docs/REWARDS.md).
- **Closing an Issue is not a production claim.** Issue state records that acceptance criteria passed, not that the network can serve the capability.
- **Confidentiality first.** Private diagnostics, hidden evaluation material and customer data never appear in Issues, PRs, logs or artifacts.

## Changing the rules

Changes to claim, reward or disclosure rules ship as a pull request that updates the code, its tests and the matching documents together. At least one maintainer other than the author reviews it. Reward terms already locked into an active claim are never altered retroactively.

## Conduct and security

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md).

# Telegraph Bounties

<img src="assets/social-preview.png" alt="Telegraph Bounties — Build the missing pieces of the machine-intelligence market" width="100%">

## The public work board for the Telegraph network.

Telegraph is a peer-to-peer ranking protocol for machine intelligence. This repository lists **what the network is missing** (a Provider, an Evaluator, an app, evaluation material, an integration) so builders can pick a gap, fix it and show proof.

> **Gap found → public Issue → builder claims → builds → submits proof → maintainer verifies → capability gets stronger.**

No reward exists unless an Issue says so. **At launch, no bounty is funded.** Funded rewards, when they appear, are written on the Issue with the amount, asset and rules before anyone can claim them.

This repository does **not** contain Telegraph's private core protocol, and it is not a vulnerability-disclosure program. See [SECURITY.md](SECURITY.md) for the latter.

---

## What can be built

Every gap on the board is one of these:

| Gap | What it means | Label |
|---|---|---|
| **Miner / Provider** | Missing, weak or unreliable intelligence supply for an Intent | `work:miner` |
| **Evaluator: adapter** | Missing or weak scoring logic (a Category-level WASM adapter) | `work:evaluator` |
| **Evaluator: material** | Missing or stale test material and independently supported references | `work:evaluator` |
| **App / Agent / integration** | An application that cannot finish its workflow because something is missing | `work:app` |
| **Tooling / protocol** | SDKs, examples, docs, observability, reliability | `work:tooling`, `work:protocol` |
| **Security hardening** | Public, non-sensitive hardening of this repository's tooling | `work:security` |
| **Release coverage** | A major AI release that the network cannot yet measure fairly | `source:release` |

Miners and Evaluators work **per Intent**, independent of industry. Apps work **per mission**. One good contribution can unblock several apps at once.

## How a bounty works

1. **Pick** an Issue labelled `status:open`.
2. **Read** the acceptance criteria and the `## Reward` section before writing code.
3. **Claim** it by commenting `/claim`. One claimant per Issue.
4. **Build** the smallest thing that meets the criteria. Post `/progress <update>` at least every 72 hours or the claim is released.
5. **Submit** proof with `/submit <links and evidence>`.
6. A maintainer reproduces your result, then runs `/approve` or returns it with `/changes <reason>`.

A bounty is done when its acceptance criteria are **reproducibly met**, not when code exists. Closing an Issue does not by itself make an Intent or Provider eligible on the network. Details: [CONTRIBUTING.md](CONTRIBUTING.md).

## Start here

| I want to… | Go to |
|---|---|
| See what to work on first | [P0 bounties](../../issues?q=is%3Aissue+is%3Aopen+label%3Apriority%3Ap0+label%3Astatus%3Aopen) |
| Pick an easy task | [Good first bounties](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+bounty%22+label%3Astatus%3Aopen) |
| Build a Miner / Provider | [Miner work](../../issues?q=is%3Aissue+is%3Aopen+label%3Awork%3Aminer+label%3Astatus%3Aopen) |
| Build an Evaluator, adapter or material | [Evaluator work](../../issues?q=is%3Aissue+is%3Aopen+label%3Awork%3Aevaluator+label%3Astatus%3Aopen) · [Evaluation needs](docs/EVALUATION_NEEDS.md) |
| Unblock an App or Agent | [App work](../../issues?q=is%3Aissue+is%3Aopen+label%3Awork%3Aapp+label%3Astatus%3Aopen) |
| Browse Season II (H2) work | [H2 gaps](../../issues?q=is%3Aissue+is%3Aopen+label%3Asource%3Ah2) · [How Season II works](docs/H2.md) |
| Browse customer and mainnet gaps | [Customer](../../issues?q=is%3Aissue+is%3Aopen+label%3Asource%3Acustomer) · [Mainnet](../../issues?q=is%3Aissue+is%3Aopen+label%3Asource%3Amainnet) |
| Report a new gap | [Open a gap report](../../issues/new/choose) |
| Cover an important AI release | [Release coverage](docs/RELEASE_COVERAGE.md) |
| Explore the Intent catalogue | [103 Intents](docs/INTENTS.md) · [Mission map](docs/MISSIONS.md) · [Reuse map](docs/NETWORK_MAP.md) |
| Look up a term | [Glossary](docs/GLOSSARY.md) |
| Find all documentation | [Docs index](docs/README.md) |
| Use this repo from an agent or script | [AGENTS.md](AGENTS.md) · [Integration](docs/INTEGRATION.md) |

Provider recruitment listings (`opportunity:provider`) invite already-operating services to talk about onboarding. They are **not** claimable bounties.

## Explore from the command line

The catalogue commands need only Python 3 and no network. On Windows use `tb.cmd` instead of `./tb`.

```bash
./tb map                          # missions and their Intents
./tb mission exchange             # one mission's Intents
./tb intent SANCTIONS_SCREENING_MATCH
./tb search weather
```

Live board commands need the [GitHub CLI](https://cli.github.com/) signed in (`gh auth login`):

```bash
./tb next                         # open claimable bounties, P0 first
./tb claim 42
./tb progress 42 "Provider is live; wiring the reference request set now."
./tb submit 42 "https://github.com/you/project: live demo + request IDs in README"
```

## Rewards

A reward exists **only when the Issue defines it**, using these fields: amount, denomination, payout asset, an explicit conversion rule when they differ, one award per Issue, eligibility, verification condition and payout window. The reward text is hashed and locked into your claim when you `/claim`, so later edits cannot change what you accepted.

No implied token amounts. Nothing here promises compensation unless an Issue states it. See [docs/REWARDS.md](docs/REWARDS.md).

## What the board will not do

- Create speculative Issues. Every gap starts from real demand, an observed failure or a verified release.
- Publish private customer data, hidden evaluation material or per-Intent weaknesses. See [SECURITY.md](SECURITY.md) and [docs/DEMAND_INTAKE.md](docs/DEMAND_INTAKE.md).
- Treat an Issue as proof of a paying buyer, a funded reward or a production-ready capability.
- Change protocol state. GitHub coordinates work; the Telegraph network decides eligibility and rankings.

## Project health

| | |
|---|---|
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Governance and roles | [GOVERNANCE.md](GOVERNANCE.md) |
| Security reports | [SECURITY.md](SECURITY.md) |
| Code of conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Getting help | [SUPPORT.md](SUPPORT.md) |
| License | [MIT](LICENSE) |

## For maintainers and operators

```bash
python scripts/prepush.py    # validate structure, data, docs and run all tests (what CI runs)
npm test                     # tests only
make seed-h2                 # publish only approved Season II seed items
make launch-check            # offline gate: refuses to pass with an empty board
```

Runbooks live in [docs/maintainers](docs/maintainers/README.md): triage, launch, GitHub settings and the evaluation pipeline. **Never announce an empty bounty board.**

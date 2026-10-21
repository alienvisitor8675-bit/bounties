# Contributing

The fastest path is an existing bounty issue.

## 1. Pick `status:open`

Claim issues marked `status:open`. Triage reports remain proposals until a maintainer turns them into clear, verifiable work.

Prefer:

- `priority:p0`
- `priority:p1`
- `help wanted`
- `good first bounty`

## 2. Claim it

Comment:

```text
/claim
```

The bot records the claimant and moves the issue to `status:claimed`.

A claim reserves the Issue while work is active. Post meaningful progress at least once every 72 hours:

```text
/progress Provider endpoint is live; integrating the reference fixtures now.
```

Stale claims are warned, then automatically released.

To return the Issue for another contributor:

```text
/release
```

## 3. Build against the acceptance criteria

Build to the acceptance checklist rather than the Issue title alone.

For Provider/Miner or Evaluator work, provide working evidence. When an Issue requires live Telegraph integration, the submission must serve or evaluate the specified Intent and pass the stated checks.

For App work, match the requested proof. Issues that require a live paid request, receipt, settlement, autonomous flow or other end-to-end evidence need a working demonstration.

## 4. Submit proof

Comment:

```text
/submit <link(s) and concise proof>
```

Example:

```text
/submit https://github.com/alice/weather-miner — live endpoint + three Telegraph request IDs + reference-test output in README
```

The issue moves to `status:review`.

## 5. Verification

A maintainer reproduces the acceptance criteria.

- Pass: `/approve`
- Needs changes: maintainer uses `/changes <reason>`; the issue returns to `status:claimed` with the same claimant and a fresh 72-hour progress window.
- Cannot continue: `/release`

Funded rewards follow the terms recorded when the active claim was created. The bot stores a visible snapshot and hash of the Issue's `## Reward` section at `/claim` time; payout also requires independent funding authorization.

## Reporting a new gap

Use the Issue chooser. Describe:

1. what useful outcome is blocked or what verified time-sensitive market coverage is missing;
2. evidence that the gap is real;
3. the reusable Intent/component involved, if known;
4. what observable result would close it.

For a major model/API/tool release, include the canonical release source, use existing Intents where they fit, and define success as fair measurement rather than a preferred rank. See [docs/RELEASE_COVERAGE.md](docs/RELEASE_COVERAGE.md).

Maintainers normalize proposals into the smallest reusable bounty.

## Contributing evaluation material

Use the [Evaluation material issue form](.github/ISSUE_TEMPLATE/evaluation-material-gap.yml) for an evidenced gap, or pick a verified open Issue. A public Issue should identify the **Category and general evaluation approach**. Handle affected Intents, adapter/profile IDs, detailed coverage weaknesses, hidden questions and exact qualification targets through an authorized private reviewer workflow. Submit material through V2 admission and qualification when applicable; Canonical Evaluator state is managed by the protocol rather than GitHub.

Use independent evidence when available, preserve upstream source provenance and distinguish verified reference observations from synthetic labels. Keep hidden sampling questions and expected answers in the authorized review system. An unranked Intent may still be routable and should display that status accurately.

The bounty repo aggregates repeated compatible Intent gaps rather than generating millions of issues. See [docs/EVALUATION_NEEDS.md](docs/EVALUATION_NEEDS.md).

## Contribution quality

This repository expects focused, verifiable contributions:

- search open and closed Issues before proposing work;
- claim only work you can actively execute;
- run and inspect generated code before submission;
- provide authentic request IDs, transactions, benchmarks and screenshots;
- propose a new Intent only for a reusable intelligence primitive;
- report exploitable vulnerabilities through the private security channel.

Repeated low-signal behavior may be closed without review.

## Security

Follow [SECURITY.md](SECURITY.md) for secrets and exploitable vulnerability details.


## Evaluation vulnerability and material disclosure

Keep public proposals at a nonsensitive Category level. Share exact affected Intent IDs, test distributions, missing reference counts, source concentration, hidden qualification inputs and answers, private diagnostic links, and customer payloads with authorized maintainers through the channel in [SECURITY.md](SECURITY.md). Maintainers verify sensitive scope privately before opening or approving funded work.

## Demand and Provider opportunities

New requests begin in triage. Anjoman and user needs require prior authorization and a sanitized public description; see [Demand intake](docs/DEMAND_INTAKE.md). Keep private prompts, files, customer identity, hidden evaluator cases and exploitable weaknesses in their authorized systems.

`opportunity:provider` Issues invite established independent services to discuss onboarding. They use the listed commercial contact path instead of the `/claim` development workflow. Other `status:open` bounties follow the claim, submit and verification process above.

## Pull requests

Most bounty deliverables—a Miner, Evaluator or App—live in **your own repository**. Submit their proof through `/submit` on the Issue. Open a pull request here when changing this repository itself:

- catalogue fixes in `catalog/` (then run `python scripts/generate_docs.py`);
- a proposed gap in `seed/h2-bounties.json` (it stays `publish: false` until a maintainer approves it);
- fixes to `tb`, the bounty workflows, validation scripts or tests;
- documentation and fictional examples under `examples/`;
- a bounty whose Issue explicitly asks for a change here: reference it with `Closes #123`.

Keep these materials out of public pull requests:

- evaluation material, hidden cases or qualification data;
- private diagnostics, customer data, credentials or exploit details;
- edits to reward terms or approvals;
- bulk generated changes nobody asked for.

Run `python scripts/prepush.py` before pushing. CI runs the same check on Linux and Windows.

The bot receipt confirms that a command was accepted. A maintainer may rerun the
original canceled or failed command job; replay protection prevents a second claim
from the same accepted command. Editing a comment does not issue another command.
Every submission requires approval from a maintainer other than its claimant and
submitter.

## Working on this repository itself

Changes to scripts, workflows, schemas or docs follow normal pull-request flow (see [GOVERNANCE.md](GOVERNANCE.md)).

Requirements: Python 3.10+ and Node.js 20+. No other dependencies.

```bash
npm test                      # JS and Python tests
python scripts/prepush.py     # full structural check (what CI runs)
python scripts/generate_docs.py   # regenerate docs/INTENTS.md, MISSIONS.md, NETWORK_MAP.md after editing catalog/
```

On Windows use `tb.cmd` (or `python tb`) in place of `./tb`. `make` is optional; every target wraps the commands above.

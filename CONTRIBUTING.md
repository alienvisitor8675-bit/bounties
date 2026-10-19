# Contributing

The fastest path is an existing bounty issue.

## 1. Pick `status:open`

Do not claim `status:triage` issues. Triage reports are proposals until a maintainer turns them into clear, verifiable work.

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

A claim coordinates work; it does not create permanent ownership. Post meaningful progress at least once every 72 hours:

```text
/progress Provider endpoint is live; integrating the reference fixtures now.
```

Stale claims are warned, then automatically released.

If you cannot continue:

```text
/release
```

## 3. Build against the acceptance criteria

Do not optimize for the issue title. Optimize for the checklist.

For Provider/Miner or Evaluator work, a repository existing is not proof. If the issue requires live Telegraph integration, it must actually serve/evaluate the specified Intent and pass the stated checks.

For App work, a mock is not enough when the issue requires a live paid request, receipt, settlement, autonomous flow or other end-to-end evidence.

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

Funded rewards are handled according to the reward terms locked when the active claim was created. The bot snapshots the Issue's `## Reward` section at `/claim` time.

## Reporting a new gap

Use the Issue chooser. Describe:

1. what useful outcome is blocked or what verified time-sensitive market coverage is missing;
2. evidence that the gap is real;
3. the reusable Intent/component involved, if known;
4. what observable result would close it.

For a major model/API/tool release, include the canonical release source and use existing Intents where they fit. Do not invent demand or require a particular ranking outcome. See [docs/RELEASE_COVERAGE.md](docs/RELEASE_COVERAGE.md).

Maintainers normalize proposals into the smallest reusable bounty.

## Contributing evaluation material

Use the [Evaluation material issue form](.github/ISSUE_TEMPLATE/evaluation-material-gap.yml) for an evidenced gap, or pick a verified open Issue. Describe only the **public Category and general evaluation approach** in a GitHub Issue. Specific affected Intents, adapter/profile IDs, material/evidence gaps, freshness/source weaknesses, hidden questions and exact qualification targets must remain within an authorized private reviewer workflow. Submit actual material through V2 admission/qualification when applicable; a GitHub PR alone cannot change Canonical Evaluator state.

Use independent evidence when available, preserve upstream source provenance and distinguish verified reference observations from synthetic labels. Never expose hidden sampling questions/expected answers. An unranked Intent may still be routable, but must not display an invented quality ranking.

The bounty repo aggregates repeated compatible Intent gaps rather than generating millions of issues. See [docs/EVALUATION_NEEDS.md](docs/EVALUATION_NEEDS.md).

## Anti-slop rule

This repo is deliberately strict because incentives attract low-quality submissions.

Do not:

- open duplicate or speculative issues without evidence;
- claim many bounties and sit on them;
- submit generated code you have not run;
- fabricate request IDs, transactions, benchmarks or screenshots;
- turn every application output into a new Intent;
- disclose exploitable vulnerabilities publicly.

Repeated low-signal behavior may be closed without review.

## Security

Follow [SECURITY.md](SECURITY.md). Never publish secrets or exploitable vulnerability details.


## Evaluation vulnerability and material disclosure

Keep public proposals Category-level and nonsensitive. Do not include exact vulnerable Intent IDs, test distributions, missing reference counts, source concentration, hidden qualification inputs/answers, private diagnostic links or customer payloads. Share sensitive diagnostics with authorized maintainers by a secure private channel (see `SECURITY.md`). Public issue forms are designed for generalized contribution proposals; maintainers verify scope privately before opening/approving funded work.

## Demand and Provider opportunities

New requests are **not automatically funded or claimable**. Anjoman/user needs require prior authorization and a sanitized, non-sensitive public description; see [Demand intake](docs/DEMAND_INTAKE.md). Do not post private prompts, files, customer identity, real hidden evaluator cases, or exploitable weaknesses to prove a gap.

`opportunity:provider` Issues invite already-operating independent services to discuss onboarding. They are commercial recruitment leads, **not** `/claim` development bounties. Follow the public contact instructions instead. For normal `status:open` bounties without that label, the existing claim/submit/verification rules remain unchanged.

## Pull requests

Most bounty deliverables (a Miner, an Evaluator, an App) live in **your own repository**. Prove them with `/submit` on the Issue; do not open a PR here for them.

Open a pull request to this repository when the change is to the repository itself:

- catalogue fixes in `catalog/` (then run `python scripts/generate_docs.py`);
- a proposed gap in `seed/h2-bounties.json` (it stays `publish: false` until a maintainer approves it);
- fixes to `tb`, the bounty workflows, validation scripts or tests;
- documentation and fictional examples under `examples/`;
- a bounty whose Issue explicitly asks for a change here: reference it with `Closes #123`.

Pull requests will be closed or redirected if they contain:

- evaluation material, hidden cases or qualification data (a PR cannot change Canonical Evaluator state, and publishing it would leak it);
- private diagnostics, customer data, credentials or exploit details;
- edits to reward terms or approvals;
- bulk generated changes nobody asked for.

Run `python scripts/prepush.py` before pushing. CI runs the same check on Linux and Windows.

## Working on this repository itself

Changes to scripts, workflows, schemas or docs follow normal pull-request flow (see [GOVERNANCE.md](GOVERNANCE.md)).

Requirements: Python 3.10+ and Node.js 20+. No other dependencies.

```bash
npm test                      # JS and Python tests
python scripts/prepush.py     # full structural check (what CI runs)
python scripts/generate_docs.py   # regenerate docs/INTENTS.md, MISSIONS.md, NETWORK_MAP.md after editing catalog/
```

On Windows use `tb.cmd` (or `python tb`) in place of `./tb`. `make` is optional; every target wraps the commands above.

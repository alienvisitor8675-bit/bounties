# Launching the repo

The repository can be structurally push-ready before it is **announcement-ready**.

## Before the first public push

Run:

```bash
make prepush
```

This checks the repo structure, catalogue references, generated docs, security contact, schemas and basic automation files.

## Before announcing the repo

Run:

```bash
make launch-check
```

The offline check inspects the **H2 seed file only** and is suitable before the initial Issue publication. Once the GitHub board has actual live customer/mainnet/H2 opportunities, use:

```bash
make launch-check-live  # requires gh login and correct GitHub repository selection
```

The live check validates **open claimable Issues** from all approved sources. It excludes commercial Provider recruitment and triage proposals, so the permanent board can grow beyond H2 seed data. This structural gate complements the separate reviews for consent, revenue and production readiness. Both routes require approved work.

### Minimum before launch

- at least **5 approved publishable bounties**;
- at least **2 P0/P1 bounties** with obvious network impact;
- at least **2 `good first bounty` tasks**;
- every funded bounty has complete reward terms;
- `/claim`, `/progress`, `/release`, `/submit`, `/approve` tested on a disposable Issue;
- security-sensitive work uses the private reporting path;
- custom GitHub social preview uploaded;
- repo pinned on the Telegraph organization/profile;
- Telegraph/Explorer/Anjoman discovery surfaces link to relevant filtered work where suitable; H2 remains an optional filter;
- launch post features specific available work and links to the repository.

## First 20 seconds

A new visitor should understand:

1. what Telegraph Bounties is;
2. why the work matters;
3. what they can build;
4. where the easiest task is;
5. where the highest-impact task is.

## First five minutes

A developer should be able to:

1. browse the 103 Intents;
2. see which missions use an Intent;
3. find one open bounty;
4. read objective acceptance criteria;
5. claim it without asking a maintainer what to do.

## How completed bounties spread

Every completed bounty should create a shareable story:

> `WEATHER_FORECAST_VERIFY` had weak supply → 3 builders added independent Providers → evaluation separated them → 4 live Apps were unblocked.

Release coverage can create equally concrete proof:

> Major model version launched → release integration gap was closed → normal evaluation ran → the measured rank/result became public.

Lead with the verified market change and use the closed Issue as its evidence.

For release-linked proof, distinguish an immutable historical event receipt from a live current-rank object. Historical proof should carry the measurement context and timestamp/round; live objects must update or expire as state changes.

That compounds better than star requests alone.

## GitHub discoverability

Configure:

- repository description;
- homepage;
- topics;
- Discussions;
- social preview;
- pinned repository;
- clear LICENSE.

Suggested topics:

`ai`, `agents`, `machine-intelligence`, `bounties`, `open-source`, `developer-tools`, `web3`, `hackathon`.

## Stars

Keep participation independent of star counts and use real deadlines when urgency exists.

Ask the existing community to star or watch **after** the repository contains useful public work. The repository should also serve readers who never claim a bounty.

Measure the repository by usefulness, repeat visits, contributions and shareable proof. Those qualities create the conditions for organic growth.

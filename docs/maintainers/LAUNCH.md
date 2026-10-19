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

The live check validates **actual open claimable Issues** from all approved sources (not commercial Provider recruitment and not speculative triage), so a permanent board is not artificially limited by H2 seed count. It is a structural data gate, not proof of consent, revenue or production readiness. Both routes require real approved issues; neither fabricates launch tasks.

### Minimum before launch

- at least **5 approved publishable bounties**;
- at least **2 P0/P1 bounties** with obvious network impact;
- at least **2 `good first bounty` tasks**;
- every funded bounty has complete reward terms;
- `/claim`, `/progress`, `/release`, `/submit`, `/approve` tested on a disposable Issue;
- no security-sensitive task exposed publicly;
- custom GitHub social preview uploaded;
- repo pinned on the Telegraph organization/profile;
- Telegraph/Explorer/Anjoman discovery surfaces link to relevant filtered work where suitable; H2 remains an optional filter;
- launch post shows actual work, not only the repository URL.

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

The story is the verified market change, not merely that an Issue closed.

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

Do not gate anything behind stars or manufacture urgency.

Ask the existing community to star/watch **after** the repository contains genuinely useful public work. The repo should deserve the star even from someone who never claims a bounty.

No architecture can guarantee a star count. The job of the repository is to maximize usefulness, repeat visits, contributions and shareable proof.

# Security Policy

**Do not open a public GitHub Issue for an exploitable vulnerability, secret, private key, credential, bypass, or sensitive infrastructure detail.**

## Report a vulnerability

Email:

**info@telegraphprotocol.com**

Use the subject:

```text
[SECURITY] Telegraph vulnerability report
```

Include only the minimum information needed to establish impact in the first message. The Telegraph team can coordinate a safer channel for additional material.

If this repository has GitHub private vulnerability reporting enabled, you may use the **Security** tab instead.

## Scope

In scope for reports to this repository:

- the bounty command and stale-claim workflows (`.github/workflows`, `scripts/*.js`), including anything that lets an unauthorised user claim, approve, release or alter reward terms;
- the evaluation-opportunity and publication scripts (`scripts/*.py`), including any path that could expose private diagnostics, hidden material or the publication key;
- leaked credentials, keys or private data in the repository or its history.

Out of scope here: the private Telegraph protocol implementation, deployed network components and third-party services. Report those through the same email and the team will route them.

## Good-faith research

Please avoid accessing, modifying or destroying data that is not yours, avoid degrading service for others, and stop and report as soon as you confirm an issue. Give the team reasonable time to respond before any public disclosure.

## Rewards

This policy does not establish a bug-bounty program. Eligibility for any reward is decided only by explicit terms communicated for a specific report. Do not assume a reward unless one has been stated.

Public Issues may be used for non-sensitive hardening work **after** sensitive details are removed or the underlying vulnerability is fixed.

## Evaluation-gap disclosure boundary

Treat per-Intent evaluation diagnostics as **internal** even when they are derived from public chain data. Do **not** copy raw node/indexer snapshots, profile thresholds, exact source concentration, missing-case distributions, stale-material details, request examples, score instability reports, or hidden qualification content into Issues, comments, pull requests, build logs, or GitHub artifacts.

Public automated opportunities may include only a broadly published Category, generic invitation to contribute compatible evaluation methods/material, review-only/unfunded status, and an opaque keyed identifier. The publisher enforces a strict schema and requires a stable private `TELEGRAPH_BOUNTY_PUBLICATION_KEY` for live GitHub creation. Keep the key in the protected operator/CI secret store; never in Git history or artifacts. Restrict raw telemetry to an authorized indexer and minimize upstream collection. A GitHub approval is **not** a decision that an evaluation is accurate.

These restrictions cannot conceal anything that V2 already makes publicly reconstructable on-chain. They limit **additional** disclosure through this repository; genuine resistance to adversarial evaluation also requires adequate data provenance, independent qualification and non-public sampling where supported.

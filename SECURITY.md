# Security Policy

**Report exploitable vulnerabilities, secrets, credentials, bypasses and sensitive infrastructure details privately.**

## Report a vulnerability

Email:

**info@telegraphprotocol.com**

Use the subject:

```text
[SECURITY] Telegraph vulnerability report
```

In the first message, include the minimum information needed to establish impact. The Telegraph team will coordinate a secure channel for additional material.

If this repository has GitHub private vulnerability reporting enabled, you may use the **Security** tab instead.

## Scope

In scope for reports to this repository:

- the bounty command and stale-claim workflows (`.github/workflows`, `scripts/*.js`), including anything that lets an unauthorised user claim, approve, release or alter reward terms;
- the evaluation-opportunity and publication scripts (`scripts/*.py`), including any path that could expose private diagnostics, hidden material or the publication key;
- leaked credentials, keys or private data in the repository or its history.

For the private Telegraph protocol, deployed network components and third-party services, use the same email and the team will route the report.

## Good-faith research

Limit testing to accounts and data you control, preserve service availability, and stop once you confirm the issue. Report promptly and allow reasonable time for a response before public disclosure.

## Rewards

This is a vulnerability-disclosure policy rather than a standing bug-bounty program. A report qualifies for a reward only when Telegraph provides explicit terms for that report.

Public Issues may be used for non-sensitive hardening work **after** sensitive details are removed or the underlying vulnerability is fixed.

## Evaluation-gap disclosure boundary

Treat per-Intent evaluation diagnostics as **internal** even when derived from public chain data. Keep raw node/indexer snapshots, profile thresholds, source concentration, missing-case distributions, stale-material details, request examples, score-instability reports and hidden qualification content out of Issues, comments, pull requests, build logs and GitHub artifacts.

Public automated opportunities contain a broad Category, a general invitation to contribute compatible evaluation methods or material, review-only/unfunded status, and an opaque keyed identifier. The publisher enforces this schema and requires a stable private `TELEGRAPH_BOUNTY_PUBLICATION_KEY` for live GitHub creation. Store the key in the protected operator environment, outside Git history and artifacts. Restrict raw telemetry to an authorized indexer and minimize upstream collection. Evaluation accuracy is decided through the protocol review process rather than GitHub approval.

Information already reconstructable from V2's public chain remains public. These controls limit additional disclosure through this repository; resistance to adversarial evaluation also depends on strong data provenance, independent qualification and private sampling where supported.

# Demand → contribution → usable capability

This repository is the **public contribution queue**, not the private Anjoman job database, commercial CRM, a payment authority, or a live protocol registry. H2 is just `source:h2`; real customer/mainnet, application, release and ongoing needs use the same reviewed queue.

## Two different requests

- **Private customer/Anjoman job:** owned by the requesting account. Full prompt, documents, contact, budget, files, provider/measurement diagnostics and job state stay in authorized systems. The customer may save a blocked request and opt into notification. There is no direct public publishing from a chat submission.
- **Public opportunity:** a maintainer-approved, sanitized, reusable gap with honest, public-safe acceptance criteria. A public opportunity can attract a Provider or contributor without identifying a customer, leaking private evaluations or implying a funded bounty.

## Qualify and publish manually

1. Verify the need: a buyer-approved requirement, failed authorized App/job, current network gap or important verifiable external release. Check whether an existing Intent/service can already solve it; don't create an Intent per user prompt.
2. Choose a route. **Existing independent service to onboard:** `opportunity:provider` (commercial recruitment, not claimable). **Reusable implementation:** normal Provider adapter, Evaluator, integration, tooling, reliability, security or protocol bounty. **Private security/evaluation vulnerability:** never place sensitive specifics in public GitHub.
3. Secure actual authorization for every fact that could identify a customer or reveal sensitive telemetry. Rewrite into the **minimum public-safe** description. No raw prompts, documents, identifiable request/response examples, private budgets, exploitable weakness, hidden evaluator cases, per-Intent diagnostic deficits or private monitoring thresholds. Synthetic examples are allowed only if clearly labeled and non-sensitive.
4. Create a `status:triage` Issue. Confirm it isn't a duplicate; mark source (`source:customer`, `source:mainnet`, `source:h2`, `source:release`, etc.) **only after verifying that source**. Specify scope, public-safe acceptance, accountable reviewer and reward status. `source:customer` does not mean a customer is publicly named or has already paid.
5. Use `/open` only for approved, reproducible bounty work. Commercial Provider opportunities may be `status:open` for outreach but have **no `/claim`/`/submit`/award lifecycle**; outreach and commercial terms are handled outside GitHub.
6. After delivery, reproduce the change and then verify actual Intent registration, eligible Provider/Evaluator state, routing, payment and **the original authorized App/job**. A closed Issue or published code does not trigger job execution or a rank change. Notify the account through its own system, subject to permissions and **fresh authorization** for paid or side-effectful work.

## Privacy-preserving integration boundary

An external authorized product may propose **only a sanitized candidate** to its private operations queue: opaque correlation token, broad capability/task category, reusable success criteria, approximate authorized demand band if needed, consent/permission record and review status. This repository does not expose an ingestion API, automatically publish issues from Anjoman, accept live customer payloads, or fetch internal node/evaluation measurements. Operators may triage and publish safe work from that queue using existing Issue Forms. Keep the private correlation token out of public Issues if it can be used to re-identify a job.

No public notification should say a capability is available merely because a bounty was claimed/closed. The **authoritative production system** must independently prove availability and eligibility. The original customer then decides whether to retry; do not auto-charge or run a dormant job on a repo event.

## Public proof, not confidential demand

A useful completion can later create a customer-approved Explorer outcome or other public result: what became available, version/time, what was verified and a supported next action (Use, Compete, Evaluate, Solve). Never publish a user's private job/result by default. Label historical outcomes as historical, distinguish internal/bootstrapped traffic from genuine external paid usage, and do not invent earnings, savings, rankings or funded demand. Shareable proof is optional and downstream of verification.

## Priority and responsibility

Prioritize concrete authorized paid-production blockers, then credible reusable application gaps and important time-sensitive market coverage. Maintainership verifies/publicizes safe work; engineering validates actual production readiness; commercial staff own buyer permission and Provider recruitment; Finance/CEO approves reward commitments. GitHub coordinates contributions—it does not decide those outcomes.

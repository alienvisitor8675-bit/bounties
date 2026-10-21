# Integration / machine-readable interface

Telegraph Bounties exposes shared data for the H2 site and other clients, with GitHub as the single work queue.

## Static catalogue

- `catalog/intents.json`
- `catalog/missions.json`

These are versioned with the repository.

## Live bounty state

GitHub Issues are the canonical live work queue.

Recommended consumers query Issues by labels:

```text
status:open
priority:p0
work:miner
work:evaluator
mission:exchange
source:h2
source:release
```

Seeded Issues contain a hidden marker:

```html
<!-- telegraph-bounty
{"intent":"WEATHER_FORECAST_VERIFY","work_type":"miner","priority":"p0", ...}
-->
```

The visible Issue body and acceptance criteria remain authoritative.

## H2 site integration

The H2 site can read the canonical catalogue and live Issue state directly.

It can display:

- mission → Intent dependencies from `catalog/missions.json`;
- live open gaps from GitHub Issues;
- links back to the canonical Issue for claiming/submission.

That preserves one source of truth while allowing the H2 site to present a mission-oriented UI.

## Release-coverage integration

Clients may query `source:release` to surface time-sensitive market-coverage work separately from H2/customer/mainnet gaps. The work/gap labels still describe the actual technical primitive, and the visible Issue acceptance criteria remain authoritative.

## Category/Intent evaluation need integration

See [EVALUATION_NEEDS.md](EVALUATION_NEEDS.md). An authorized protocol or Explorer read model provides detailed observations to the private operator pipeline. `scripts/evaluation_opportunities.py` groups them internally, and `scripts/evaluation_publication.py` produces the strict public Category-level projection.

Public consumers can ingest `opportunities[].id`, `category_id`, `work_type`, `review_status` and `funded_reward`, then link to reviewed GitHub triage Issues through the stable `telegraph-eval-opportunity` marker. The public projection intentionally omits adapter and profile IDs, gaps, affected Intents, samples, demand counters and rankings.

The H2 site, Explorer and bounty repository can share this generated index. GitHub Issues remain canonical for **work** state, while Telegraph remains authoritative for protocol state. This repository includes the pipeline and fixtures; operators connect it to the approved upstream system during deployment.

## Continuous customer/Anjoman demand integration

See [DEMAND_INTAKE.md](DEMAND_INTAKE.md). This repository has no Anjoman webhook or API. Private saved customer jobs stay in Anjoman; an authorized operator may publish a sanitized, reviewed capability opportunity. The `source:customer` label identifies an approved source and does not authorize disclosure of customer details.

- **Input boundary:** the product stores the job and consent record and determines whether the request is unsupported. An authorized operator creates a sanitized `status:triage` Issue; prompts, files, customer data and evaluation diagnostics stay in their source systems.
- **Work boundary:** `opportunity:provider` uses the commercial Provider recruitment path. Standard `work:*` Issues cover reusable code and evaluation work with explicit reward status. `source:h2` is one optional source filter.
- **Output boundary:** GitHub `status:done` means the Issue acceptance criteria passed. The production network establishes Intent and Provider eligibility and whether an Anjoman job can run. Anjoman owns job notifications and reauthorization.
- **Explorer boundary:** a public result requires verification, dated context, accurate source and operator attribution, and user approval. Customer deliverables remain in the customer system, and test traffic is identified as test traffic.

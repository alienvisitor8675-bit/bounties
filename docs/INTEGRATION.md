# Integration / machine-readable interface

Telegraph Bounties is designed so the H2 site or another client can consume the same underlying data without duplicating the bounty system.

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

The H2 site should not maintain a second bounty database.

It can display:

- mission → Intent dependencies from `catalog/missions.json`;
- live open gaps from GitHub Issues;
- links back to the canonical Issue for claiming/submission.

That preserves one source of truth while allowing the H2 site to present a mission-oriented UI.

## Release-coverage integration

Clients may query `source:release` to surface time-sensitive market-coverage work separately from H2/customer/mainnet gaps. The work/gap labels still describe the actual technical primitive, and the visible Issue acceptance criteria remain authoritative.

## Category/Intent evaluation need integration

See [EVALUATION_NEEDS.md](EVALUATION_NEEDS.md). An authorized external protocol/Explorer read model publishes **non-secret** evaluation profile descriptions and per-Intent observed counters in JSON + NDJSON. `scripts/evaluation_opportunities.py` produces compact grouped opportunity IDs. This is not an alternative to the live Intent state, a production oracle, or a source of qualified Consumer demand on its own.

Consumers can ingest the generated `opportunities[].id`, `category_id`, `adapter_id`, `profile_id`, `gap`, `affected_intents`, sampled IDs, available demand counters and `review_status`, then link to reviewed GitHub triage Issues by the stable `telegraph-eval-opportunity` marker. Do not display review candidates as funded/approved bounties or live rankings.

The H2 site, Explorer and bounty repo can share this generated index, while GitHub Issues remain the canonical **work** state and Telegraph remains the source of truth for protocol state. This ZIP does not connect a live upstream feed.

## Continuous customer/Anjoman demand integration

See [DEMAND_INTAKE.md](DEMAND_INTAKE.md). **No Anjoman webhook or API is implemented in this ZIP**. Private saved customer jobs must stay outside public GitHub; only an authorized, sanitized, reviewed capability opportunity may be published. `source:customer` is an approved public classification, not authorization to quote the customer.

- **Input boundary:** product stores job/consent and determines whether the request is genuinely unsupported. An authorized operator may create a sanitized `status:triage` Issue; no raw prompt/files, private customer data or evaluation diagnostics.
- **Work boundary:** `opportunity:provider` is a commercial Provider recruitment path, never a claimable bounty. Standard `work:*` Issues are verified reusable code/evaluation work with explicit reward status. `source:h2` is only one optional source filter.
- **Output boundary:** GitHub `status:done` means the stated Issue acceptance passed. Only the production network can attest that a suitable Intent/Provider is eligible and that the blocked Anjoman job is runnable. Job notifications and reauthorization live in Anjoman, not GitHub.
- **Explorer boundary:** a result may be shared only with suitable verification, dated context, correct source/operator attribution and user approval. A public bounty issue must not embed customer deliverables or imply production usage from test traffic.

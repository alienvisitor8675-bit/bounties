# Glossary

Terms as this repository uses them. Protocol behaviour is defined by Telegraph itself; where this glossary and the protocol differ, the protocol wins.

| Term | Meaning |
|---|---|
| **Intent** | A reusable machine-intelligence task with a market of its own, such as `WEATHER_FORECAST_VERIFY`. The catalogue lists 103 ([INTENTS.md](INTENTS.md)). Miners and Evaluators compete per Intent. |
| **Category** | A group of related Intents, such as Climate & Weather. Evaluation scoring logic can be shared across a Category. |
| **Mission** | One of the 15 Season II application goals. A mission composes several Intents. A mission is application logic, not a new Intent ([MISSIONS.md](MISSIONS.md)). |
| **Season II / H2** | The hackathon proving ground built around the 15 missions. `source:h2` marks work that comes from it. H2 is one filter on the board, not the whole board ([H2.md](H2.md)). |
| **Miner / Provider** | A service that supplies intelligence for an Intent. The GitHub label stays `work:miner`; public text often says Provider. |
| **Evaluator** | A party that measures how good supplied intelligence is so Miners can be ranked. |
| **Canonical Evaluator** | The Evaluator the protocol currently recognises for an Intent. It is set by the protocol's own competition and verification, never by this repository or by catalogue metadata. |
| **Adapter** | Category-level scoring logic (WASM) that compatible Intents can reuse. Qualification and ranking remain per Intent. |
| **Evaluation material** | Task examples and independently supported reference answers used to test Miners. Hidden qualification material stays secret. See [EVALUATION_NEEDS.md](EVALUATION_NEEDS.md). |
| **App / Agent** | A product or autonomous workflow that consumes Intents. Apps create demand and expose gaps. |
| **Gap** | Something the network needs that is missing or too weak: supply, evaluation, integration, tooling or release coverage. A gap becomes a public Issue only after maintainer triage. |
| **Bounty** | A claimable Issue (`status:open`) with objective acceptance criteria. It may or may not carry a reward. |
| **Provider opportunity** | `opportunity:provider`. A commercial recruitment listing for an already-operating service. Not claimable and never a bounty. |
| **Slot Issue** | One of several related Issues (1/3, 2/3, 3/3) used when the network needs several independent implementations. Each has its own claim and reward terms. |
| **Triage** | The first state of every public report (`status:triage`). A maintainer checks it is real, reusable, not a duplicate, safe to publish and verifiable before running `/open`. |
| **Claim** | The exclusive right to work an Issue, recorded by the bot. It is released after 72 hours without a `/progress` update. |
| **Release coverage** | Work that lets a newly released model, API or tool be measured fairly in an existing market. Success is fair eligibility, not a particular rank. See [RELEASE_COVERAGE.md](RELEASE_COVERAGE.md). |
| **Anjoman** | Telegraph's job product. Its jobs, documents and budgets are private and never published here. See [DEMAND_INTAKE.md](DEMAND_INTAKE.md). |
| **Explorer** | Telegraph's view of network state. This repository does not read from it directly. |
| **MACHINA** | A possible bounty payout asset. A reward counts only if the Issue names the asset and the conversion rule ([REWARDS.md](REWARDS.md)). |
| **V2** | The current Telegraph protocol generation referred to by the evaluation documents. |

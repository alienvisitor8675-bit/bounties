# Intent Catalogue

**103 reusable machine-intelligence capabilities.**

This is the public H2 catalogue used by Telegraph Bounties. Intents are reusable intelligence markets; missions may compose several of them.

> Mission usage is a starting coordination map, not a restriction. Apps may use any relevant Intent.

> **Important:** `evaluation_mechanism` and `scoring_path` are H2/reference coordination metadata. They are **not** immutable Canonical Evaluators or permanent protocol state. Telegraph's live Canonical Evaluator for an Intent is determined by the protocol's competitive Evaluator-selection and verification process and may change over time.

## AI & Machine Learning

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `LLM_OUTPUT_EVALUATION` | mandatory | NON-DETERMINISTIC | < 3s | Model Economy |
| `LANGUAGE_TRANSLATION` | existing | NON-DETERMINISTIC | < 1.5s | Consumer Platform, Personal Agent |
| `QUESTION_ANSWERING` | existing | HYBRID | < 2s | Institutional Markets, Legal, Consumer Platform, Personal Agent, Model Economy |
| `TEXT_SUMMARIZATION` | existing | NON-DETERMINISTIC | < 3s | Personal Agent |
| `WEB_SEARCH_QUERY` | existing | HYBRID | < 800ms | Institutional Markets, Legal, Conflict Intelligence, Commodities, Personal Agent, Model Economy |
| `CHATBOT_CONVERSATION` | existing | NON-DETERMINISTIC | < 1.5s | — |
| `ENTITY_EXTRACTION` | existing | HYBRID | < 600ms | — |
| `INTENT_CLASSIFICATION` | existing | HYBRID | < 300ms | — |
| `SEMANTIC_SIMILARITY` | existing | DETERMINISTIC | < 250ms | — |
| `SENTIMENT_ANALYSIS` | existing | HYBRID | < 300ms | — |
| `SPEECH_TO_TEXT` | existing | HYBRID | < 4s | — |
| `TEXT_CLASSIFICATION` | existing | HYBRID | < 400ms | — |
| `URL_CONTENT_EXTRACTION` | existing | DETERMINISTIC | < 2s | Personal Agent |
| `EMBEDDING_GENERATION` | existing | DETERMINISTIC | < 200ms | — |
| `IMAGE_CAPTIONING` | existing | NON-DETERMINISTIC | < 2.5s | Consumer Platform, Autonomous Systems |
| `KEYWORD_EXTRACTION` | existing | HYBRID | < 400ms | — |
| `TEXT_TO_SPEECH` | existing | NON-DETERMINISTIC | < 3s | — |

### Details

#### `LLM_OUTPUT_EVALUATION`

Evaluates generative model responses against factual ground truth, citation fidelity, hallucination markers, and safety guardrails.

Priority: **9** · Scoring path: `adapter only` · Verification complexity: **High**

#### `LANGUAGE_TRANSLATION`

Translates multilingual text between source and target language pairs preserving semantic intent and idiom.

Priority: **8** · Scoring path: `adapter only` · Verification complexity: **High** · Evaluation: `COMET / BLEU Metric Comparator`

#### `QUESTION_ANSWERING`

Answers open-domain and context-bounded user queries with cited factual assertions and logical deductions.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **High** · Evaluation: `Factuality Rubric & LLM-as-Judge`

#### `TEXT_SUMMARIZATION`

Generates concise, factual executive summaries capturing primary themes of long-form source documents.

Priority: **8** · Scoring path: `adapter only` · Verification complexity: **High** · Evaluation: `LLM-as-Judge & BERTScore`

#### `WEB_SEARCH_QUERY`

Executes programmatic web search queries and returns top ranked organic URLs, snippets, and knowledge graphs.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Rank Correlation (NDCG / Spearman)`

#### `CHATBOT_CONVERSATION`

Maintains multi-turn conversational context, tone alignment, and empathetic response delivery.

Priority: **7** · Scoring path: `adapter only` · Verification complexity: **High** · Evaluation: `Multi-Turn CSAT & Safety Rubric`

#### `ENTITY_EXTRACTION`

Extracts named entities (people, organizations, locations, dates) with character offsets from unstructured text.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Span-Level F1 Score`

#### `INTENT_CLASSIFICATION`

Classifies user natural language input into downstream system action intents and extracts slot arguments.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Top-1 Intent Match & Slot F1`

#### `SEMANTIC_SIMILARITY`

Calculates mathematical cosine similarity and semantic relatedness distance between pairs of sentences.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `SENTIMENT_ANALYSIS`

Scores emotional valence, polarity (positive/negative/neutral), and subjective tone in textual messages.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Probability Distribution Alignment`

#### `SPEECH_TO_TEXT`

Transcribes spoken audio streams into punctuated, timestamped text transcriptions with speaker diarization.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Word Error Rate (WER) Comparator`

#### `TEXT_CLASSIFICATION`

Assigns predefined taxonomic category tags and topic hierarchies to incoming text documents.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Multi-Engine Voting Consensus`

#### `URL_CONTENT_EXTRACTION`

Scrapes target web pages, cleans boilerplate DOM nodes, and extracts clean markdown article content.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Text Diff & Token Overlap`

#### `EMBEDDING_GENERATION`

Transforms input text strings into standardized high-dimensional float vector embeddings for retrieval systems.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Vector Epsilon Comparator`

#### `IMAGE_CAPTIONING`

Generates descriptive, contextual alt-text captions describing the primary subjects and scenes in image files.

Priority: **6** · Scoring path: `adapter only` · Verification complexity: **High** · Evaluation: `CLIPScore & CIDEr Metric`

#### `KEYWORD_EXTRACTION`

Extracts representative topical keywords, keyphrases, and n-grams from body text.

Priority: **6** · Scoring path: `comparator + adapter` · Verification complexity: **Low** · Evaluation: `Jaccard Index & Rank Overlap`

#### `TEXT_TO_SPEECH`

Synthesizes natural-sounding spoken voice waveforms from text input with adjustable emotion and cadence.

Priority: **6** · Scoring path: `adapter only` · Verification complexity: **High** · Evaluation: `MOS / NISQA Perceptual Score`

## Blockchain & Web3

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `CROSS_CHAIN_STATE_VERIFY` | mandatory | DETERMINISTIC | < 3s | Stablecoin |
| `EVENT_OUTCOME_RESOLUTION` | mandatory | HYBRID | < 5s | Web3 Native & DeFi |
| `LIQUIDITY_DEPTH_VERIFY` | mandatory | DETERMINISTIC | < 500ms | Exchange, Stablecoin, Institutional Markets, Asset Management, Web3 Native & DeFi |
| `ONCHAIN_METRIC_VERIFY` | mandatory | DETERMINISTIC | < 2s | Exchange, Asset Management, Web3 Native & DeFi |
| `WASH_TRADING_DETECTION` | mandatory | HYBRID | < 4s | Exchange, Asset Management, Web3 Native & DeFi |
| `ASSET_RESERVE_ATTESTATION` | mandatory | DETERMINISTIC | < 5s | Stablecoin, Mining & Power, Asset Management |
| `CRYPTO_PRICE_LOOKUP` | existing | DETERMINISTIC | < 400ms | Asset Management |
| `CRYPTO_TRANSFER_VERIFY` | existing | DETERMINISTIC | < 1.5s | Web3 Native & DeFi |
| `SMART_CONTRACT_AUDIT` | existing | HYBRID | < 8s | Exchange, Web3 Native & DeFi |
| `CRYPTO_YIELD_RATE` | existing | DETERMINISTIC | < 1.2s | Asset Management |
| `GAS_PRICE_ESTIMATION` | existing | DETERMINISTIC | < 500ms | — |
| `TOKEN_TOTAL_SUPPLY_VERIFY` | existing | DETERMINISTIC | < 500ms | Exchange |
| `VALIDATOR_PERFORMANCE_VERIFY` | mandatory | DETERMINISTIC | < 1.5s | Mining & Power, Asset Management |

### Details

#### `CROSS_CHAIN_STATE_VERIFY`

Proves cryptographic Merkle-Patricia state roots and cross-chain message execution headers between distinct blockchain networks.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **High**

#### `EVENT_OUTCOME_RESOLUTION`

Resolves objective real-world event outcomes for prediction markets and conditional contracts using quorum oracles.

Priority: **10** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `LIQUIDITY_DEPTH_VERIFY`

Measures bid-ask order book depth, cumulative slippage bands, and market maker liquidity across decentralized pools.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `ONCHAIN_METRIC_VERIFY`

Validates smart contract event logs, gas consumption, token balances, and wallet transaction states directly on-chain.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `WASH_TRADING_DETECTION`

Analyzes DEX transaction graphs and circular transfer loops between affiliated wallets to identify artificial trade volume.

Priority: **10** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `ASSET_RESERVE_ATTESTATION`

Verifies cryptographic proof-of-reserves and custodial bank confirmations backing stablecoins and tokenized assets.

Priority: **9** · Scoring path: `comparator only` · Verification complexity: **High**

#### `CRYPTO_PRICE_LOOKUP`

Fetches real-time spot and volume-weighted average prices for crypto assets across major exchanges.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `CRYPTO_TRANSFER_VERIFY`

Verifies on-chain transaction status, gas fee burn, sender/recipient addresses, and block confirmations.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Medium** · Evaluation: `Exact Match Comparator`

#### `SMART_CONTRACT_AUDIT`

Inspects bytecode and smart contract source code for reentrancy, access control, and integer overflows.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **High** · Evaluation: `Multi-Engine Heuristic Scoring`

#### `CRYPTO_YIELD_RATE`

Tracks annualized percentage yields (APY), staking reward rates, and lending pool yields across DeFi protocols.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium** · Evaluation: `Numeric Tolerance Comparator`

#### `GAS_PRICE_ESTIMATION`

Estimates dynamic base fee, tip priority, and gas limits across standard transaction speed tiers.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `TOKEN_TOTAL_SUPPLY_VERIFY`

Verifies token circulating supply, burnt token balances, and total minted token counts on-chain.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Exact Match Comparator`

#### `VALIDATOR_PERFORMANCE_VERIFY`

Tracks consensus voting uptime, proposed block rates, slashing penalties, and staking APR for network validators.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Climate & Weather

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `AIR_QUALITY_INDEX` | existing | DETERMINISTIC | < 800ms | — |
| `WEATHER_CURRENT` | existing | DETERMINISTIC | < 600ms | — |
| `WEATHER_FORECAST_VERIFY` | mandatory | DETERMINISTIC | < 1s | Conflict Intelligence, Resources & Agriculture, Commodities, Autonomous Systems, Mining & Power |

### Details

#### `AIR_QUALITY_INDEX`

Aggregates particulate matter (PM2.5/PM10), ground ozone, and composite AQI metrics from monitoring stations.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `WEATHER_CURRENT`

Provides real-time ambient temperature, humidity, precipitation rate, and wind vectors by coordinates.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `WEATHER_FORECAST_VERIFY`

Reconciles localized Doppler radar feeds, barometric pressure, wind gusts, and severe weather alert bulletins.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Low**

## Commerce & Procurement

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `COMMERCE_PURCHASE_VERIFY` | mandatory | DETERMINISTIC | < 1s | Consumer Automation |
| `LIVE_SHELF_PRICE` | mandatory | DETERMINISTIC | < 2s | Consumer Platform, Consumer Automation |
| `SKU_IN_STOCK` | mandatory | DETERMINISTIC | < 500ms | Consumer Platform, Consumer Automation |
| `PURCHASE_ORDER_VERIFY` | mandatory | DETERMINISTIC | < 2s | — |
| `VENDOR_VERIFY` | mandatory | HYBRID | < 3s | — |
| `PRODUCT_AUTHENTICITY` | mandatory | HYBRID | < 3s | Consumer Platform, Consumer Automation |
| `RETURN_POLICY_VERIFY` | mandatory | HYBRID | < 800ms | — |
| `SHIP_RATE_ETA` | mandatory | HYBRID | < 1s | Resources & Agriculture, Commodities, Personal Agent |

### Details

#### `COMMERCE_PURCHASE_VERIFY`

Verifies the authenticity, item line totals, and payment authorization for a completed e-commerce purchase transaction.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `LIVE_SHELF_PRICE`

Fetches and verifies current live shelf or retail listing prices across online merchant catalogs and marketplaces.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `SKU_IN_STOCK`

Confirms real-time stock availability, quantities, and warehouse fulfillment readiness for a given SKU.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `PURCHASE_ORDER_VERIFY`

Reconciles enterprise purchase orders with procurement approval workflows, vendor quotas, and budget allocations.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `VENDOR_VERIFY`

Audits vendor tax identifiers, compliance credentials, banking details, and sanctions list clearance.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `PRODUCT_AUTHENTICITY`

Validates product provenance, serial numbers, and manufacturer anti-counterfeit records against authorized registries.

Priority: **6** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `RETURN_POLICY_VERIFY`

Validates order return eligibility, restocking fees, and merchant policy constraints based on purchase timestamp and category.

Priority: **6** · Scoring path: `comparator + adapter` · Verification complexity: **Low**

#### `SHIP_RATE_ETA`

Calculates and verifies carrier shipping rates, service tiers, and estimated delivery dates for specified zip codes.

Priority: **6** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

## Cybersecurity

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `VULNERABILITY_TRIAGE` | mandatory | HYBRID | < 2s | Model Economy, Web3 Native & DeFi |
| `EMAIL_SECURITY` | mandatory | HYBRID | < 500ms | — |
| `MALWARE_DETECTION` | mandatory | HYBRID | < 4s | — |
| `THREAT_INTELLIGENCE` | mandatory | HYBRID | < 1s | — |
| `THREAT_IP_REPUTATION` | existing | HYBRID | < 400ms | — |
| `URL_SAFE` | mandatory | HYBRID | < 300ms | Consumer Platform, Consumer Automation |
| `DNS_RECORD_LOOKUP` | existing | DETERMINISTIC | < 200ms | — |
| `PORT_SCAN_AUDIT` | existing | DETERMINISTIC | < 2s | — |
| `SSL_CERTIFICATE_VERIFY` | existing | DETERMINISTIC | < 500ms | — |

### Details

#### `VULNERABILITY_TRIAGE`

Ranks and categorizes detected vulnerabilities by CVSS score, active exploit availability, and asset criticality.

Priority: **10** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `EMAIL_SECURITY`

Verifies SPF, DKIM, and DMARC records, inspects header anomalies, and detects spoofing or malicious attachments.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `MALWARE_DETECTION`

Scans file hashes and binaries against multi-engine antivirus definitions and sandbox behavioral detonation traces.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `THREAT_INTELLIGENCE`

Aggregates indicators of compromise (IOCs), malicious IP ranges, and adversary tactics from global security feeds.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `THREAT_IP_REPUTATION`

Assesses malicious IP address risk scores, botnet associations, and brute-force history across threat registries.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Consensus Scoring Comparator`

#### `URL_SAFE`

Checks target URLs against live threat feeds, DNS blocklists, phishing databases, and domain reputation monitors.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Low**

#### `DNS_RECORD_LOOKUP`

Resolves and validates authoritative DNS records (A, AAAA, CNAME, MX, TXT) across global resolvers.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Exact Match Comparator`

#### `PORT_SCAN_AUDIT`

Identifies open network service ports, banner disclosures, and listening daemon protocols on specified hosts.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium** · Evaluation: `Exact Match Comparator`

#### `SSL_CERTIFICATE_VERIFY`

Validates TLS/SSL certificate chains, cipher suites, expiration dates, and revocation statuses.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Deterministic Rule Validator`

## Energy & Infrastructure

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `CLOUD_RESOURCE_USAGE` | existing | DETERMINISTIC | < 1s | — |
| `DATACENTER_TELEMETRY_VERIFY` | mandatory | DETERMINISTIC | < 2s | Autonomous Systems, Mining & Power |
| `GRID_POWER_PRICE` | mandatory | DETERMINISTIC | < 1s | Resources & Agriculture, Autonomous Systems, Mining & Power |
| `MINING_HASHPRICE_VERIFY` | mandatory | DETERMINISTIC | < 1s | Mining & Power |

### Details

#### `CLOUD_RESOURCE_USAGE`

Audits virtual machine and container compute utilization, memory pressure, and network throughput metrics.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium** · Evaluation: `Numeric Tolerance Comparator`

#### `DATACENTER_TELEMETRY_VERIFY`

Audits rack power usage effectiveness (PUE), server thermal telemetry, and backup generator readiness metrics.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `GRID_POWER_PRICE`

Ingests real-time nodal marginal locational prices (LMP) and day-ahead electricity spot rates from regional grid operators.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `MINING_HASHPRICE_VERIFY`

Calculates instantaneous proof-of-work mining revenue per unit of hashing power based on block rewards and network difficulty.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Enterprise Operations

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `B2B_IDENTITY_ENRICHMENT` | mandatory | HYBRID | < 2s | Institutional Markets, Personal Agent |
| `CONTRACT_OBLIGATION_AUDIT` | mandatory | NON-DETERMINISTIC | < 4s | Legal |
| `DOCUMENT_AUTHENTICITY` | mandatory | HYBRID | < 2.5s | Stablecoin, Institutional Markets, Legal, Commodities |
| `INVOICE_LEDGER_RECONCILE` | mandatory | HYBRID | < 3s | — |
| `API_HEALTH_CHECK` | existing | DETERMINISTIC | < 400ms | — |
| `CUSTOMER_TICKET_RESOLUTION` | mandatory | NON-DETERMINISTIC | < 1.5s | — |
| `SERVER_UPTIME_MONITOR` | existing | DETERMINISTIC | < 600ms | Consumer Automation |
| `SLA_COMPLIANCE` | mandatory | DETERMINISTIC | < 1s | Mining & Power, Consumer Automation |

### Details

#### `B2B_IDENTITY_ENRICHMENT`

Enriches business entity records with corporate tax IDs, headquarters addresses, executive listings, and domain validation.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `CONTRACT_OBLIGATION_AUDIT`

Parses and verifies legal contract milestone deliverables, payment terms, and vendor performance commitments.

Priority: **8** · Scoring path: `adapter only` · Verification complexity: **High**

#### `DOCUMENT_AUTHENTICITY`

Validates digital certificate signatures, notarizations, tamper-evident seals, and document checksum integrity.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `INVOICE_LEDGER_RECONCILE`

Performs automated 3-way matching between invoice line items, purchase orders, and receiving dock receipts.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `API_HEALTH_CHECK`

Verifies REST/GraphQL API responsiveness, JSON schema payload structure, and HTTP status codes.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `JSON Schema Validator`

#### `CUSTOMER_TICKET_RESOLUTION`

Analyzes helpdesk support interactions, resolution accuracy, agent action compliance, and customer satisfaction outcomes.

Priority: **6** · Scoring path: `adapter only` · Verification complexity: **Medium**

#### `SERVER_UPTIME_MONITOR`

Monitors synthetic HTTP/HTTPS endpoint availability, handshake latency, and uptime status from multiple edge regions.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Exact Match Comparator`

#### `SLA_COMPLIANCE`

Measures operational response and resolution turnaround against contractually agreed enterprise service level agreements.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Financial / Transactional

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `OPTIMAL_EXECUTION_ROUTE` | mandatory | HYBRID | < 150ms | — |
| `FRAUD_RISK` | mandatory | NON-DETERMINISTIC | < 350ms | Stablecoin |
| `PAYMENT_METHOD_VERIFY` | mandatory | DETERMINISTIC | < 600ms | Stablecoin |
| `TRANSACTION_RISK` | mandatory | NON-DETERMINISTIC | < 250ms | Stablecoin, Mining & Power |
| `FX_NOW` | mandatory | DETERMINISTIC | < 200ms | Stablecoin, Institutional Markets, Commodities, Personal Agent |
| `CREDIT_SCORE_VERIFY` | existing | HYBRID | < 800ms | — |
| `CURRENCY_EXCHANGE` | existing | DETERMINISTIC | < 250ms | — |
| `STOCK_PRICE_QUOTE` | existing | DETERMINISTIC | < 350ms | Asset Management |
| `LOAN_INTEREST_RATE_QUOTE` | existing | DETERMINISTIC | < 1s | — |

### Details

#### `OPTIMAL_EXECUTION_ROUTE`

Determines optimal multi-venue order execution routing to minimize slippage, exchange fees, and market impact.

Priority: **10** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `FRAUD_RISK`

Computes real-time behavioral fraud probability scores using device fingerprinting, IP geolocation, and transaction context.

Priority: **9** · Scoring path: `adapter only` · Verification complexity: **High**

#### `PAYMENT_METHOD_VERIFY`

Verifies card BIN validity, tokenization credentials, bank account routing, and active account standing.

Priority: **9** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `TRANSACTION_RISK`

Evaluates cardholder spending velocity, merchant categorization codes, and chargeback history to score transaction risk.

Priority: **9** · Scoring path: `adapter only` · Verification complexity: **High**

#### `FX_NOW`

Provides real-time institutional foreign exchange mid-market rates, spreads, and currency conversion quotes.

Priority: **8** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `CREDIT_SCORE_VERIFY`

Validates consumer credit bureau score ranges, adverse factors, and debt-to-income benchmarks.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Scored Range Comparator`

#### `CURRENCY_EXCHANGE`

Calculates fiat currency conversion rates and mid-market spot pricing across global currency pairs.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `STOCK_PRICE_QUOTE`

Retrieves live and official market-close equity quotes, bid-ask spreads, and trading volume.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

#### `LOAN_INTEREST_RATE_QUOTE`

Aggregates residential mortgage APRs, prime lending rates, and personal loan interest quotes.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Numeric Tolerance Comparator`

## Geospatial & Remote Sensing

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `SATELLITE_IMAGERY_ANALYSIS` | mandatory | NON-DETERMINISTIC | < 12s | Conflict Intelligence, Resources & Agriculture, Autonomous Systems |

### Details

#### `SATELLITE_IMAGERY_ANALYSIS`

Processes multispectral satellite feeds for land use changes, crop vegetation indexes, and infrastructure monitoring.

Priority: **5** · Scoring path: `adapter only` · Verification complexity: **High**

## IoT & Telemetry

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `SENSOR_TELEMETRY_VERIFY` | mandatory | DETERMINISTIC | < 400ms | Resources & Agriculture, Autonomous Systems, Mining & Power |

### Details

#### `SENSOR_TELEMETRY_VERIFY`

Validates edge sensor heartbeat signals, cryptographic payload integrity, and calibration threshold bounds.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Legal & Compliance

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `KYC_BIOMETRIC_LIVENESS` | mandatory | HYBRID | < 2s | — |
| `SANCTIONS_SCREENING_MATCH` | mandatory | HYBRID | < 500ms | Exchange, Stablecoin, Institutional Markets, Legal, Conflict Intelligence, Commodities |
| `CORPORATE_REGISTRY_LOOKUP` | mandatory | DETERMINISTIC | < 2.5s | Institutional Markets, Legal, Asset Management |
| `REGULATORY_FILING_MONITOR` | mandatory | DETERMINISTIC | < 3s | Legal, Asset Management |

### Details

#### `KYC_BIOMETRIC_LIVENESS`

Verifies user selfie liveness video capture against government photo IDs to prevent spoofing fraud.

Priority: **9** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `SANCTIONS_SCREENING_MATCH`

Screens counterparties and beneficial owners against OFAC, EU, and UN consolidated financial sanctions lists.

Priority: **9** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `CORPORATE_REGISTRY_LOOKUP`

Queries national business registers for incorporation status, registered agent details, and beneficial ownership filings.

Priority: **8** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `REGULATORY_FILING_MONITOR`

Parses statutory regulatory filings, 10-K/10-Q disclosures, and disclosure updates from financial oversight portals.

Priority: **8** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Logistics

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `CARRIER_SERVICEABILITY` | mandatory | DETERMINISTIC | < 600ms | — |
| `DELIVERY_WINDOW_VERIFY` | mandatory | DETERMINISTIC | < 800ms | Consumer Platform, Consumer Automation |
| `PACKAGE_STATUS` | mandatory | DETERMINISTIC | < 500ms | — |
| `SHIPMENT_DELAY_RISK` | mandatory | NON-DETERMINISTIC | < 2s | — |
| `WAREHOUSE_INVENTORY` | mandatory | DETERMINISTIC | < 1s | Autonomous Systems |

### Details

#### `CARRIER_SERVICEABILITY`

Evaluates freight and courier delivery coverage, weight limits, and hazardous material restrictions for target routes.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `DELIVERY_WINDOW_VERIFY`

Confirms driver dispatch route scheduling, customer delivery appointment slots, and signature requirements.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `PACKAGE_STATUS`

Tracks real-time parcel checkpoint milestones, courier custody transfers, and delivery progress across logistics carriers.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `SHIPMENT_DELAY_RISK`

Assesses predictive delay risk based on customs processing times, port congestion, weather conditions, and transport nodes.

Priority: **5** · Scoring path: `adapter only` · Verification complexity: **High**

#### `WAREHOUSE_INVENTORY`

Audits bin and pallet level stock counts, pick-and-pack allocations, and replenishment thresholds in fulfillment centers.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Logistics & Maritime

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `LIVE_PORT_CONGESTION` | mandatory | HYBRID | < 3s | Conflict Intelligence, Resources & Agriculture, Commodities |
| `VESSEL_TELEMETRY_VERIFY` | mandatory | DETERMINISTIC | < 1.5s | Stablecoin, Conflict Intelligence, Resources & Agriculture, Commodities |

### Details

#### `LIVE_PORT_CONGESTION`

Measures commercial container port vessel queue wait times, berth occupancy ratios, and dwell day averages.

Priority: **5** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `VESSEL_TELEMETRY_VERIFY`

Ingests maritime AIS positioning transponder data to track vessel speed, draft, bunker fuel burn, and nautical headings.

Priority: **5** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Macroeconomics & Finance

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `MACRO_ECONOMIC_INDICATOR` | mandatory | DETERMINISTIC | < 2s | Institutional Markets, Conflict Intelligence, Commodities, Mining & Power, Asset Management |

### Details

#### `MACRO_ECONOMIC_INDICATOR`

Aggregates released central bank interest rates, consumer price index (CPI) updates, and unemployment figures.

Priority: **8** · Scoring path: `comparator only` · Verification complexity: **Low**

## Software / Engineering

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `CODE_PATCH_VERIFY` | mandatory | DETERMINISTIC | < 10s | Model Economy |
| `CODE_REVIEW` | mandatory | NON-DETERMINISTIC | < 5s | Model Economy |
| `SECURITY_REVIEW` | mandatory | HYBRID | < 8s | Exchange, Model Economy, Web3 Native & DeFi |
| `CODE_GENERATION` | existing | HYBRID | < 4s | Personal Agent, Model Economy |
| `REGRESSION_VERIFY` | mandatory | DETERMINISTIC | < 15s | Model Economy |
| `TASK_EXECUTION_QUALITY` | mandatory | NON-DETERMINISTIC | < 2s | Personal Agent, Autonomous Systems |
| `GRAMMAR_SPELL_CHECK` | existing | DETERMINISTIC | < 350ms | — |

### Details

#### `CODE_PATCH_VERIFY`

Validates that software patch commits compile, resolve targeted defects, and introduce no regression side effects.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **High**

#### `CODE_REVIEW`

Evaluates source code pull requests against internal architectural patterns, maintainability standards, and syntax rules.

Priority: **10** · Scoring path: `adapter only` · Verification complexity: **High**

#### `SECURITY_REVIEW`

Scans codebase dependencies, API endpoints, and configuration files for common CVEs, secrets leakage, and misconfigurations.

Priority: **10** · Scoring path: `comparator + adapter` · Verification complexity: **High**

#### `CODE_GENERATION`

Generates executable, type-safe code snippets and algorithms meeting specified functional specifications.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **High** · Evaluation: `Unit Test Pass Rate + LLM Review`

#### `REGRESSION_VERIFY`

Runs automated test suite executions to confirm backward compatibility across modified service APIs and libraries.

Priority: **7** · Scoring path: `comparator only` · Verification complexity: **High**

#### `TASK_EXECUTION_QUALITY`

Benchmarks automated job or agent execution outputs against gold-standard rubrics and expected schema constraints.

Priority: **7** · Scoring path: `adapter only` · Verification complexity: **Medium**

#### `GRAMMAR_SPELL_CHECK`

Detects typographical, orthographic, punctuation, and grammatical syntax errors with correction offsets.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low** · Evaluation: `Rule Match Comparator`

## Travel & Mobility

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `TRAVEL_DISRUPTION` | mandatory | DETERMINISTIC | < 1s | Consumer Automation |
| `FARE_RULE_VERIFY` | mandatory | HYBRID | < 800ms | — |
| `FLIGHT_AVAILABILITY` | mandatory | DETERMINISTIC | < 1s | — |
| `HOTEL_AVAILABILITY` | mandatory | DETERMINISTIC | < 1.2s | — |
| `ROUTE_ETA` | mandatory | DETERMINISTIC | < 500ms | Resources & Agriculture, Autonomous Systems |
| `TRAVEL_TRANSIT_LOCK` | mandatory | DETERMINISTIC | < 1.5s | — |

### Details

#### `TRAVEL_DISRUPTION`

Detects and monitors flight delays, cancellations, gate shifts, and weather-driven travel disruptions in real time.

Priority: **10** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `FARE_RULE_VERIFY`

Inspects fare terms, baggage allowances, cancellation penalties, and change fee stipulations for booked travel tickets.

Priority: **6** · Scoring path: `comparator + adapter` · Verification complexity: **Medium**

#### `FLIGHT_AVAILABILITY`

Queries real-time airline schedule networks, cabin seat inventories, and booking fare class statuses.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `HOTEL_AVAILABILITY`

Confirms room inventory, nightly rates, amenities, and cancellation policies across hospitality property management systems.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium**

#### `ROUTE_ETA`

Computes multimodal routing itineraries, live traffic transit times, and turn-by-turn arrival estimations.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Low**

#### `TRAVEL_TRANSIT_LOCK`

Verifies and confirms fare holds, ticket reservation guarantees, and transit seat locking mechanisms.

Priority: **6** · Scoring path: `comparator only` · Verification complexity: **Medium**

## Trust & Safety

| Intent | Tier | Class | Latency | Used by H2 missions |
|---|---|---|---|---|
| `FACT_CHECKING` | existing | HYBRID | < 2.5s | Legal, Conflict Intelligence, Consumer Platform |
| `MEDIA_FORENSIC_VERIFY` | mandatory | NON-DETERMINISTIC | < 6s | Conflict Intelligence, Consumer Platform |
| `TOXICITY_MODERATION` | existing | HYBRID | < 350ms | — |
| `PLAGIARISM_DETECTION` | existing | HYBRID | < 3s | — |
| `SOCIAL_BOT_DETECTION` | mandatory | NON-DETERMINISTIC | < 2s | Exchange, Consumer Platform |

### Details

#### `FACT_CHECKING`

Verifies factual claims against authoritative knowledge bases, peer-reviewed registries, and primary sources.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **High** · Evaluation: `Claim Verification Consensus`

#### `MEDIA_FORENSIC_VERIFY`

Detects AI deepfake artifacts, EXIF metadata manipulation, and generative audio/video synthesis in media uploads.

Priority: **8** · Scoring path: `adapter only` · Verification complexity: **High**

#### `TOXICITY_MODERATION`

Evaluates user submitted text for hate speech, harassment, sexual content, self-harm incitement, and toxicity.

Priority: **8** · Scoring path: `comparator + adapter` · Verification complexity: **Medium** · Evaluation: `Multi-Model Safety Consensus`

#### `PLAGIARISM_DETECTION`

Detects verbatim text duplication, disguised paraphrasing, and uncredited citations across corpus databases.

Priority: **7** · Scoring path: `comparator + adapter` · Verification complexity: **High** · Evaluation: `Shingle Overlap & Similarity Threshold`

#### `SOCIAL_BOT_DETECTION`

Classifies social media user accounts by post frequency anomalies, follower graph clusters, and coordinated inauthentic behavior.

Priority: **7** · Scoring path: `adapter only` · Verification complexity: **High**

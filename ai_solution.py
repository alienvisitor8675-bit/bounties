To solve this task, we will create a Telegraph miner that provides current war-risk insurance premium changes for a shipping region.

### Step-by-Step Explanation:

1. **Propose Intent:**
   - We'll propose a new Intent named `war-risk.insurance.rates`.

2. **YAML Configuration:**
   - We'll define the YAML configuration with the Intent, description, and function.

### Solution Code:

```yaml
openai:
  chain: "Ethereum Sepolia testnet (chain 11155111)"
  contract: "0x3624EB012B5E998BB57B6bE6C9Cfc9c4bc5eb99b"
  node: "13.237.89.59:7148"

Intents:
  - proposeIntent:
      name: war-risk.insurance.rates
      description: "war-risk insurance rates"
      de: "war-risk insurance rates"

Miner:
  - id: "war-risk.insurance.rates"

  hooks:
    - name: "war-risk.insurance.rates"
      input:
        schema:
          type: "object"
          properties:
            region:
              type: "string"
              description: "The shipping region (e.g., North Atlantic)."
      output:
        schema:
          type: "object"
          properties:
            rate:
              type: "string"
              description: "The current war-risk insurance rate."
            timestamp:
              type: "string"
              format: "date-time"
              description: "The date and time of the rate update."

  functions:
    - name: "war-risk.insurance.rates"
      template: "The current war-risk insurance rate for the region {{region}} is {{rate}} as of {{timestamp}}."
      async: true
      inputs:
        region:
          type: "string"
          required: true
      outputs:
        rate:
          type: "string"
        timestamp:
          type: "string"
```

This YAML defines a miner for the proposed Intent, including the necessary schemas and function template.
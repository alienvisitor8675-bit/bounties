```yaml
chain: 11155111
contract: 0x3624EB012B5E998BB57B6bE6C9Cfc9c4bc5eb99b
node: 13.237.89.59:7148

intent: ad-invalid-traffic-detection

mining:
  inputs:
    - name: impressions
      type: integer
      description: Number of impressions
    - name: clicks
      type: integer
      description: Number of clicks
    - name: estimatedClickThroughRate:
      type: float
      description: eCVR (estimated Click Through Rate)
  output:
    - name: estimatedShare
      type: float
      description: The estimated share of bot or invalid traffic
  formula: estimatedShare = 1 - (1 - (clicks / impressions)) ** 3
```
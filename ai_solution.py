```yaml
name: currentWildfireRisk
prompt: "What is the current wildfire risk in the given forest area?"
response: "The current wildfire risk in [forest name] is [low, moderate, high, or extreme]."
hooks:
  - name: "wildfireRisk"
    prompt: "The current wildfire risk in the given forest area depends on several factors. Please provide specific data about the forest area, such as its location, temperature, humidity, wind, and recent fire activity, to determine the risk level."
    response: "The current wildfire risk in [forest name] is [low, moderate, high, or extreme]. This assessment is based on the temperature, humidity, wind, and recent fire activity in the area."
```
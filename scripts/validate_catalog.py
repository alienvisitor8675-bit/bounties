#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


# Apply the repository's declared JSON schema first.
subprocess.run([sys.executable, str(ROOT / 'scripts/schema_check.py')], cwd=ROOT, check=True)

intents = load('catalog/intents.json')
missions = load('catalog/missions.json')
seed = load('seed/h2-bounties.json')
intent_names = {x['name'] for x in intents}
assert len(intent_names) == len(intents), 'Duplicate Intents'
assert len(intents) == 103, f'Expected 103 public H2 Intents, found {len(intents)}'
mission_ids = {m['id'] for m in missions}
assert len(mission_ids) == len(missions) == 15, 'Mission catalogue must contain 15 unique missions'

mission_by_id = {m['id']: m for m in missions}
intent_by_name = {x['name']: x for x in intents}

for x in intents:
    assert x['tier'] in {'mandatory', 'existing'}
    assert x['class'] in {'DETERMINISTIC', 'HYBRID', 'NON-DETERMINISTIC'}
    for mid in x.get('used_by_missions', []):
        assert mid in mission_ids, f"Unknown mission on {x['name']}: {mid}"
        assert x['name'] in mission_by_id[mid]['core_intents'], (
            f"Reverse map mismatch: {x['name']} says it is used by {mid}, "
            "but the mission does not list it"
        )

for m in missions:
    missing = [x for x in m['core_intents'] if x not in intent_names]
    assert not missing, f"{m['id']} references unknown Intents: {missing}"
    for name in m['core_intents']:
        assert m['id'] in intent_by_name[name].get('used_by_missions', []), (
            f"Reverse map mismatch: {m['id']} lists {name}, "
            "but the Intent does not list the mission"
        )

for item in seed:
    assert item['work_type'] in {'miner', 'evaluator', 'app', 'protocol', 'tooling', 'security'}
    assert item['priority'] in {'p0', 'p1', 'p2'}
    if item.get('intent'):
        assert item['intent'] in intent_names, f"Unknown Intent in seed: {item['intent']}"
    for mid in item.get('missions', []):
        assert mid in mission_ids, f"Unknown mission in seed: {mid}"
    assert item.get('acceptance'), f"Missing acceptance criteria: {item.get('title')}"
    reward = item.get('reward') or {}
    assert 'funded' in reward, f"Missing reward.funded: {item.get('title')}"
    assert reward.get('max_awards', 1) == 1, (
        f"One claim/award per Issue is enforced; use separate slot Issues for multiple implementations: {item['title']}"
    )
    if reward['funded']:
        for field in ['amount', 'denomination', 'payout_asset', 'eligibility', 'verification_condition', 'payout_window']:
            assert reward.get(field) not in (None, ''), f"Funded bounty missing reward.{field}: {item['title']}"
        if str(reward['denomination']).upper() != str(reward['payout_asset']).upper():
            assert reward.get('conversion_rule') not in (None, ''), (
                f"Cross-denomination funded bounty missing reward.conversion_rule: {item['title']}"
            )

mandatory = sum(1 for x in intents if x['tier'] == 'mandatory')
existing = sum(1 for x in intents if x['tier'] == 'existing')
assert (mandatory, existing) == (63, 40), f'Expected 63 mandatory + 40 existing Intents, found {mandatory} + {existing}'

print(f'OK: {len(intents)} Intents ({mandatory} mandatory + {existing} existing), {len(missions)} missions, {len(seed)} seed candidates')

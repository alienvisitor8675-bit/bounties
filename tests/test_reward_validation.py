#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from schema_check import validate_seed_item  # noqa: E402

schema = json.loads((ROOT / 'schema/bounty.schema.json').read_text(encoding='utf-8'))
base = json.loads((ROOT / 'seed/h2-bounties.json').read_text(encoding='utf-8'))[0]


def expect_fail(item, needle):
    try:
        validate_seed_item(item, schema)
    except AssertionError as exc:
        assert needle in str(exc), (needle, str(exc))
        return
    raise AssertionError(f'expected validation failure containing {needle!r}')


# One claim/award per Issue is enforced at schema level.
item = copy.deepcopy(base)
item['reward']['max_awards'] = 2
expect_fail(item, 'must equal 1')

# Cross-denomination funded rewards require an explicit conversion rule.
item = copy.deepcopy(base)
item['reward'].update({
    'funded': True,
    'amount': 500,
    'denomination': 'USD',
    'payout_asset': 'MACHINA',
    'eligibility': 'Open to eligible contributors',
    'verification_condition': 'Acceptance criteria reproduced',
    'payout_window': 'Within 14 days',
    'conversion_rule': None,
})
expect_fail(item, 'required when denomination differs from payout_asset')

# The same funded bounty is valid once conversion is explicit.
item['reward']['conversion_rule'] = 'MACHINA amount uses the 24h Ethereum TWAP at approval, rounded down to 8 decimals.'
validate_seed_item(item, schema)

print('REWARD VALIDATION TESTS OK: 3')

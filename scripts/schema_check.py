#!/usr/bin/env python3
"""Dependency-free validator for the JSON-Schema subset used by this repository."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(path, message):
    raise AssertionError(f"{path}: {message}")


def type_ok(value, expected):
    if expected == 'null': return value is None
    if expected == 'boolean': return isinstance(value, bool)
    if expected == 'string': return isinstance(value, str)
    if expected == 'number': return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == 'integer': return isinstance(value, int) and not isinstance(value, bool)
    if expected == 'object': return isinstance(value, dict)
    if expected == 'array': return isinstance(value, list)
    return False


def validate(value, schema, path='$'):
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(type_ok(value, t) for t in types):
            fail(path, f"expected type {types}, got {type(value).__name__}")

    if 'const' in schema and value != schema['const']:
        fail(path, f"must equal {schema['const']!r}")
    if 'enum' in schema and value not in schema['enum']:
        fail(path, f"must be one of {schema['enum']!r}")

    if isinstance(value, str) and 'minLength' in schema and len(value) < schema['minLength']:
        fail(path, f"length must be >= {schema['minLength']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum']:
            fail(path, f"must be >= {schema['minimum']}")

    if isinstance(value, list):
        if 'minItems' in schema and len(value) < schema['minItems']:
            fail(path, f"must contain >= {schema['minItems']} items")
        if schema.get('uniqueItems'):
            frozen = [json.dumps(v, sort_keys=True, separators=(',', ':')) for v in value]
            if len(frozen) != len(set(frozen)):
                fail(path, 'items must be unique')
        if 'items' in schema:
            for i, item in enumerate(value):
                validate(item, schema['items'], f'{path}[{i}]')

    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                fail(path, f"missing required property {key!r}")
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            extra = sorted(set(value) - set(props))
            if extra:
                fail(path, f"unexpected properties: {extra}")
        for key, item in value.items():
            if key in props:
                validate(item, props[key], f'{path}.{key}')


def validate_seed_item(item, schema, path='$'):
    validate(item, schema, path)
    reward = item.get('reward') or {}
    if reward.get('funded'):
        required = ['amount', 'denomination', 'payout_asset', 'eligibility', 'verification_condition', 'payout_window']
        for field in required:
            if reward.get(field) in (None, ''):
                fail(f'{path}.reward.{field}', 'required for funded bounty')
        if str(reward['denomination']).upper() != str(reward['payout_asset']).upper():
            if reward.get('conversion_rule') in (None, ''):
                fail(f'{path}.reward.conversion_rule', 'required when denomination differs from payout_asset')


def main():
    schema = json.loads((ROOT / 'schema/bounty.schema.json').read_text(encoding='utf-8'))
    data = json.loads((ROOT / 'seed/h2-bounties.json').read_text(encoding='utf-8'))
    for i, item in enumerate(data):
        validate_seed_item(item, schema, f'$[{i}]')
    print(f'SCHEMA OK: {len(data)} seed candidates')


if __name__ == '__main__':
    main()

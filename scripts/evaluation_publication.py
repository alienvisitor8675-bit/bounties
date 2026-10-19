#!/usr/bin/env python3
"""Strict, fail-closed public projection for internal evaluation-gap observations.

The internal gap model is *not* a GitHub publication schema. Public projection is
Category-level and intentionally hides Intent IDs, source concentration, gaps,
counts, thresholds, requirement-profile details, private URLs, and demand metrics.
"""
import hashlib
import hmac
import re

PUB_SCHEMA_VERSION = 2
PUB_KIND = 'evaluation-contributions'
PUB_SCOPE = 'public category-level review candidates only; no quality/ranking claims or funded reward'
PUB_ITEM_KEYS = frozenset({'id', 'category_id', 'work_type', 'review_status', 'funded_reward'})
PUB_TOP_KEYS = frozenset({'schema_version', 'generated_at', 'scope', 'opportunities'})
CATEGORY_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}$')
PUBLIC_ID_PATTERN = re.compile(r'^evalpub-[a-f0-9]{24}$')


def publication_key(value):
    if not isinstance(value, str) or len(value) < 32:
        raise ValueError('TELEGRAPH_BOUNTY_PUBLICATION_KEY must be a stable high-entropy secret of at least 32 characters')
    return value.encode('utf-8')


def category_id(value):
    if not isinstance(value, str) or not CATEGORY_PATTERN.fullmatch(value):
        raise ValueError('invalid public Category identifier')
    return value


def opaque_id(category, key):
    """Keyed ID avoids deterministic gap/profile fingerprints in public markers."""
    digest = hmac.new(key, b'telegraph:eval-public:v2:category\x00' + category.encode('utf-8'), hashlib.sha256)
    return 'evalpub-' + digest.hexdigest()[:24]


def publicize_opportunities(internal, secret):
    """Use *only* explicitly constructed fields. Never copy internal objects."""
    key = publication_key(secret)
    if not isinstance(internal, dict) or not isinstance(internal.get('opportunities'), list):
        raise ValueError('invalid internal opportunity state')
    categories = {category_id(item['category_id']) for item in internal['opportunities']}
    public = [{
        'id': opaque_id(cat, key),
        'category_id': cat,
        'work_type': PUB_KIND,
        'review_status': 'triage',
        'funded_reward': False,
    } for cat in sorted(categories)]
    output = {
        'schema_version': PUB_SCHEMA_VERSION,
        'generated_at': internal['generated_at'],
        'scope': PUB_SCOPE,
        'opportunities': public,
    }
    validate_public_export(output, secret)
    return output


def validate_public_export(data, secret=None):
    if not isinstance(data, dict) or set(data) != PUB_TOP_KEYS:
        raise ValueError('invalid public export keys; private state cannot be published')
    if data['schema_version'] != PUB_SCHEMA_VERSION or data['scope'] != PUB_SCOPE:
        raise ValueError('unsupported public export schema')
    if not isinstance(data.get('generated_at'), str):
        raise ValueError('invalid generation time')
    if not isinstance(data.get('opportunities'), list):
        raise ValueError('public opportunities must be a list')
    key = publication_key(secret) if secret is not None else None
    seen_ids, seen_categories = set(), set()
    for item in data['opportunities']:
        if not isinstance(item, dict) or set(item) != PUB_ITEM_KEYS:
            raise ValueError('public opportunity contains disallowed/internal fields')
        cat = category_id(item['category_id'])
        ident = item['id']
        if not isinstance(ident, str) or not PUBLIC_ID_PATTERN.fullmatch(ident):
            raise ValueError('invalid opaque public opportunity ID')
        if ident in seen_ids or cat in seen_categories:
            raise ValueError('duplicate public opportunity identity')
        seen_ids.add(ident)
        seen_categories.add(cat)
        if item['work_type'] != PUB_KIND or item['review_status'] != 'triage' or item['funded_reward'] is not False:
            raise ValueError('public export must remain generic, review-only and unfunded')
        if key is not None and not hmac.compare_digest(ident, opaque_id(cat, key)):
            raise ValueError('public opportunity ID does not match authorized publication key')
    return data['opportunities']

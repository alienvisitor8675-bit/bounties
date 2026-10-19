#!/usr/bin/env python3
"""Produce bounded, reviewable, grouped bounty opportunities from an external state export.

Never reads hidden test questions/answers; never asserts that admitted labels are true.
Pure offline tool, no GitHub mutations. Input snapshots are evidence *claims* that must
be verified by maintainers before an Issue is made claimable.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from evaluation_publication import publicize_opportunities

IDENTIFIER = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}$')
GAPS = {
    'adapter_missing': 'Compatible Category WASM evaluation logic is unavailable',
    'evaluator_missing': 'No qualified Canonical Evaluator is reported',
    'material_insufficient': 'Too little eligible evaluation material',
    'material_stale': 'Too little fresh eligible evaluation material',
    'source_diversity': 'Too few independent reference-source domains',
    'case_coverage': 'The declared evaluation cases are insufficiently covered',
    'quality_review': 'A reproducible evaluation-quality concern requires investigation',
}


def valid_id(value, field):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f'{field} must be a stable short identifier')
    return value


def nonneg_number(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not (0 <= value < float('inf')):
        raise ValueError(f'{field} must be a finite nonnegative number')
    return value


def iso_time(value):
    if not isinstance(value, str) or not value.endswith('Z'):
        raise ValueError('observed_at must be a UTC ISO 8601 timestamp ending in Z')
    try:
        return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('invalid observed_at timestamp') from exc


def load_profiles(path):
    profiles = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(profiles, list):
        raise ValueError('profiles must be a JSON list')
    result = {}
    for item in profiles:
        if not isinstance(item, dict):
            raise ValueError('profile must be an object')
        allowed_profile = {'id', 'category_id', 'adapter_id', 'material_schema', 'reference_evidence', 'min_eligible_items', 'min_fresh_items', 'min_source_domains', 'max_material_age_hours', 'min_case_coverage'}
        if set(item) != allowed_profile:
            raise ValueError('profile must contain only approved input fields')
        pid = valid_id(item.get('id'), 'profile.id')
        if pid in result:
            raise ValueError(f'duplicate profile: {pid}')
        valid_id(item.get('category_id'), 'profile.category_id')
        valid_id(item.get('adapter_id'), 'profile.adapter_id')
        if not isinstance(item.get('material_schema'), str) or not item['material_schema'].strip():
            raise ValueError(f'{pid}: missing material schema')
        if not isinstance(item.get('reference_evidence'), str) or not item['reference_evidence'].strip():
            raise ValueError(f'{pid}: missing reference evidence requirements')
        if len(item['reference_evidence']) > 1000 or len(item['material_schema']) > 200:
            raise ValueError(f'{pid}: requirement is too long')
        for key in ('min_eligible_items', 'min_fresh_items', 'min_source_domains'):
            nonneg_number(item.get(key), f'{pid}.{key}')
        for key in ('max_material_age_hours', 'min_case_coverage'):
            nonneg_number(item.get(key), f'{pid}.{key}')
        if item['min_case_coverage'] > 1:
            raise ValueError('min_case_coverage must be in [0,1]')
        result[pid] = item
    return result


def validate_snapshot(row, profiles, now, max_snapshot_hours):
    if not isinstance(row, dict):
        raise ValueError('intent record must be JSON object')
    if set(row) - {'intent_id', 'profile_id', 'observed_at', 'observed', 'demand'} or not {'intent_id', 'profile_id', 'observed_at', 'observed'} <= set(row):
        raise ValueError('intent record contains unsupported or missing input fields')
    intent = valid_id(row.get('intent_id'), 'intent_id')
    profile_id = valid_id(row.get('profile_id'), 'profile_id')
    if profile_id not in profiles:
        raise ValueError(f'{intent}: profile {profile_id} not in supplied profile registry')
    when = iso_time(row.get('observed_at'))
    age_hours = (now - when).total_seconds() / 3600
    if age_hours < -1 or age_hours > max_snapshot_hours:
        raise ValueError(f'{intent}: future or stale snapshot, age_hours={age_hours:.1f}')
    obs = row.get('observed')
    if not isinstance(obs, dict):
        raise ValueError(f'{intent}: missing observed metrics')
    if set(obs) != {'eligible_items', 'fresh_items', 'source_domains', 'case_coverage', 'qualified_evaluator_present', 'adapter_available', 'quality_alert'}:
        raise ValueError(f'{intent}: unknown or missing observed metrics')
    for k in ('eligible_items', 'fresh_items', 'source_domains', 'case_coverage', 'qualified_evaluator_present', 'adapter_available', 'quality_alert'):
        if k not in obs:
            raise ValueError(f'{intent}: missing observation {k} (do not assume zero)')
    for k in ('eligible_items', 'fresh_items', 'source_domains', 'case_coverage'):
        nonneg_number(obs[k], f'{intent}.observed.{k}')
    if obs['case_coverage'] > 1 or obs['fresh_items'] > obs['eligible_items']:
        raise ValueError(f'{intent}: inconsistent observed counters')
    for k in ('qualified_evaluator_present', 'adapter_available', 'quality_alert'):
        if type(obs[k]) is not bool:
            raise ValueError(f'{intent}.observed.{k} must be boolean')
    demand = row.get('demand', {})
    if not isinstance(demand, dict) or set(demand) - {'qualified_paid_usdc_30d', 'blocked_apps'}:
        raise ValueError(f'{intent}: demand must contain only approved aggregate metrics')
    for k in ('qualified_paid_usdc_30d', 'blocked_apps'):
        if k in demand:
            nonneg_number(demand[k], f'{intent}.demand.{k}')
    return intent, profile_id, obs, demand


def detected_gaps(obs, p):
    gaps = []
    if not obs['adapter_available']:
        gaps.append('adapter_missing')
    if not obs['qualified_evaluator_present']:
        gaps.append('evaluator_missing')
    if obs['eligible_items'] < p['min_eligible_items']:
        gaps.append('material_insufficient')
    if obs['fresh_items'] < p['min_fresh_items']:
        gaps.append('material_stale')
    if obs['source_domains'] < p['min_source_domains']:
        gaps.append('source_diversity')
    if obs['case_coverage'] < p['min_case_coverage']:
        gaps.append('case_coverage')
    if obs['quality_alert']:
        gaps.append('quality_review')
    return gaps


def compile_opportunities(profiles, path, now=None, max_snapshot_hours=168):
    now = now or dt.datetime.now(dt.timezone.utc)
    groups = {}
    seen = set()
    processed = 0
    with Path(path).open(encoding='utf-8') as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                intent, profile_id, obs, demand = validate_snapshot(row, profiles, now, max_snapshot_hours)
                if intent in seen:
                    raise ValueError(f'duplicate Intent ID in snapshot: {intent}')
                seen.add(intent)
                processed += 1
                p = profiles[profile_id]
                for gap in detected_gaps(obs, p):
                    key = (p['category_id'], p['adapter_id'], profile_id, gap)
                    if key not in groups:
                        digest = hashlib.sha256('\x1f'.join(key).encode()).hexdigest()[:16]
                        groups[key] = {
                            'id': f'evalgap-{digest}',
                            'category_id': p['category_id'], 'adapter_id': p['adapter_id'],
                            'profile_id': profile_id, 'gap': gap, 'description': GAPS[gap],
                            'requirements': {
                                'material_schema': p['material_schema'],
                                'reference_evidence': p['reference_evidence'],
                                'min_eligible_items': p['min_eligible_items'],
                                'min_fresh_items': p['min_fresh_items'],
                                'min_source_domains': p['min_source_domains'],
                                'max_material_age_hours': p['max_material_age_hours'],
                                'min_case_coverage': p['min_case_coverage'],
                            },
                            'affected_intents': 0, 'example_intents': [],
                            'known_qualified_paid_usdc_30d': 0, 'known_blocked_apps': 0,
                            'intents_with_demand_metrics': 0, 'intents_with_blocker_metrics': 0,
                            'review_status': 'triage', 'funded_reward': False,
                        }
                    item = groups[key]
                    item['affected_intents'] += 1
                    if len(item['example_intents']) < 5:
                        item['example_intents'].append(intent)
                    if 'qualified_paid_usdc_30d' in demand:
                        item['known_qualified_paid_usdc_30d'] += demand['qualified_paid_usdc_30d']
                        item['intents_with_demand_metrics'] += 1
                    if 'blocked_apps' in demand:
                        item['known_blocked_apps'] += demand['blocked_apps']
                        item['intents_with_blocker_metrics'] += 1
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                raise ValueError(f'{path}:{lineno}: {exc}') from exc
    values = sorted(groups.values(), key=lambda x: (-x['known_blocked_apps'], -x['known_qualified_paid_usdc_30d'], -x['affected_intents'], x['id']))
    return {
        'schema_version': 1, 'generated_at': now.isoformat().replace('+00:00', 'Z'),
        'processed_intents': processed, 'opportunity_count': len(values),
        'scope': 'public review candidates; not automatic bounty approval or evidence of correct rankings',
        'opportunities': values,
    }


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--profiles', required=True)
    a.add_argument('--snapshot', required=True, help='newline-delimited JSON, one observed Intent per line')
    a.add_argument('--output', help='write PUBLIC-SAFE Category-level JSON (default stdout)')
    a.add_argument('--now', help='override UTC now, for testing/archival only')
    a.add_argument('--max-snapshot-hours', type=float, default=168)
    args = a.parse_args()
    if args.max_snapshot_hours <= 0:
        a.error('--max-snapshot-hours must be positive')
    now = iso_time(args.now) if args.now else None
    # Never serialize private opportunity diagnostics to stdout or a GitHub artifact.
    # Absence of a stable secret must fail closed; rotating it breaks issue identity.
    try:
        result = compile_opportunities(load_profiles(args.profiles), args.snapshot, now, args.max_snapshot_hours)
        public = publicize_opportunities(result, os.getenv('TELEGRAPH_BOUNTY_PUBLICATION_KEY'))
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError):
        print('Evaluation export rejected: invalid source, unavailable publication key, or unsafe state. See private indexer diagnostics.', file=sys.stderr)
        raise SystemExit(2)
    serialized = json.dumps(public, indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(serialized, encoding='utf-8')
        print('Generated public Category-level opportunities (review only).')
    else:
        print(serialized, end='')


if __name__ == '__main__':
    main()

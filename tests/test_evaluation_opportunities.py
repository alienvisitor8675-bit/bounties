#!/usr/bin/env python3
"""Internal detection tests; exported projection is covered by security tests."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from evaluation_opportunities import compile_opportunities, load_profiles
from evaluation_publication import publicize_opportunities, validate_public_export

NOW = dt.datetime(2026, 10, 11, 10, 0, tzinfo=dt.timezone.utc)
PROFILES = ROOT / 'examples/evaluation-profiles.example.json'
SNAPSHOT = ROOT / 'examples/evaluation-state.example.ndjson'
KEY = 'test-publisher-secret-not-for-deployment-000000000001'


class EvaluationOpportunityTests(unittest.TestCase):
    def setUp(self):
        self.profiles = load_profiles(PROFILES)

    def test_detects_gaps_internally_but_exports_only_category(self):
        internal = compile_opportunities(self.profiles, SNAPSHOT, now=NOW)
        self.assertEqual(internal['processed_intents'], 3)
        self.assertEqual(internal['opportunity_count'], 4)
        for item in internal['opportunities']:
            self.assertEqual(item['affected_intents'], 2)
            self.assertEqual(item['known_qualified_paid_usdc_30d'], 155)
            self.assertEqual(item['known_blocked_apps'], 2)
        public = publicize_opportunities(internal, KEY)
        self.assertEqual(len(validate_public_export(public, KEY)), 1)
        self.assertEqual(public['opportunities'][0]['category_id'], 'weather-intelligence')
        self.assertEqual(public, publicize_opportunities(compile_opportunities(self.profiles, SNAPSHOT, now=NOW), KEY))
        body = json.dumps(public)
        for forbidden in ('WEATHER_FORECAST_VERIFY', 'material_stale', 'source_diversity',
                          'weather-wasm-v1', 'weather-forecast-hourly-v1', 'min_fresh_items',
                          'source_domains', 'example.org', '155', '120', '0.7'):
            self.assertNotIn(forbidden, body)

    def test_scales_by_internal_and_public_aggregation(self):
        example = json.loads(SNAPSHOT.read_text(encoding='utf-8').splitlines()[0])
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'observations.ndjson'
            with path.open('w',encoding='utf-8') as fh:
                for i in range(10000):
                    row = dict(example, intent_id=f'WEATHER_LOCATION_{i}')
                    fh.write(json.dumps(row) + '\n')
            result = compile_opportunities(self.profiles, path, now=NOW)
        self.assertEqual(result['processed_intents'], 10000)
        self.assertEqual(result['opportunity_count'], 4)
        public = publicize_opportunities(result, KEY)
        self.assertEqual(len(public['opportunities']), 1)
        self.assertNotIn('10000', json.dumps(public))

    def test_duplicate_intent_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'dupes.ndjson'
            path.write_text(SNAPSHOT.read_text(encoding='utf-8').splitlines()[0] + '\n' + SNAPSHOT.read_text(encoding='utf-8').splitlines()[0] + '\n')
            with self.assertRaisesRegex(ValueError, 'duplicate Intent'):
                compile_opportunities(self.profiles, path, now=NOW)

    def test_stale_or_missing_metrics_fail_closed(self):
        row = json.loads(SNAPSHOT.read_text(encoding='utf-8').splitlines()[0])
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'bad.ndjson'
            row['observed_at'] = '2025-01-01T00:00:00Z'
            path.write_text(json.dumps(row) + '\n')
            with self.assertRaisesRegex(ValueError, 'stale snapshot'):
                compile_opportunities(self.profiles, path, now=NOW)
            row['observed_at'] = '2026-10-11T04:00:00Z'
            del row['observed']['source_domains']
            path.write_text(json.dumps(row) + '\n')
            with self.assertRaisesRegex(ValueError, 'unknown or missing observed metrics'):
                compile_opportunities(self.profiles, path, now=NOW)

    def test_uncorroborated_alert_is_private_not_a_public_flag(self):
        row = json.loads(SNAPSHOT.read_text(encoding='utf-8').splitlines()[2])
        row['observed']['quality_alert'] = True
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'alert.ndjson'
            path.write_text(json.dumps(row) + '\n')
            internal = compile_opportunities(self.profiles, path, now=NOW)
        self.assertEqual([o['gap'] for o in internal['opportunities']], ['quality_review'])
        self.assertNotIn('quality_review', json.dumps(publicize_opportunities(internal, KEY)))


if __name__ == '__main__':
    unittest.main()

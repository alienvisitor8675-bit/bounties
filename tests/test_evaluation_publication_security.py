#!/usr/bin/env python3
"""Adversarial regression: nothing sensitive from telemetry may hit public sinks."""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from evaluation_opportunities import compile_opportunities, load_profiles, iso_time
from evaluation_publication import publicize_opportunities, validate_public_export, PUBLIC_ID_PATTERN
from sync_evaluation_issues import issue_body, issue_title, check_result

KEY = 'offline-test-private-publication-key-000000000000000001'
NOW = iso_time('2026-10-11T10:00:00Z')


class PublicationSecurityTests(unittest.TestCase):
    def setUp(self):
        self.internal = compile_opportunities(load_profiles(ROOT / 'examples/evaluation-profiles.example.json'), ROOT / 'examples/evaluation-state.example.ndjson', now=NOW)
        self.public = publicize_opportunities(self.internal, KEY)

    def test_public_schema_exact_keys_and_generic_scope(self):
        self.assertEqual(set(self.public), {'schema_version', 'generated_at', 'scope', 'opportunities'})
        self.assertEqual(len(self.public['opportunities']), 1)
        item = self.public['opportunities'][0]
        self.assertEqual(set(item), {'id', 'category_id', 'work_type', 'review_status', 'funded_reward'})
        self.assertRegex(item['id'], PUBLIC_ID_PATTERN)
        self.assertNotIn('weather-wasm-v1', json.dumps(self.public))
        self.assertNotIn('material_insufficient', json.dumps(self.public))
        self.assertNotIn('WEATHER_FORECAST_VERIFY', json.dumps(self.public))

    def test_private_fields_and_schema_one_rejected(self):
        for field, secret in [('example_intents',['SECRET_INTENT']), ('requirements',{'min_source_domains':2}),
                              ('gap','quality_review'), ('example_evidence_urls',['https://private.example/a']),
                              ('affected_intents',12), ('source_domains',1)]:
            bad = copy.deepcopy(self.public)
            bad['opportunities'][0][field] = secret
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_public_export(bad, KEY)
        original_internal = copy.deepcopy(self.internal)
        with self.assertRaises(ValueError):
            validate_public_export(original_internal, KEY)
        with self.assertRaises(ValueError):
            check_result(original_internal, NOW, 24)

    def test_private_metadata_canary_cannot_escape_output_or_issue(self):
        private = copy.deepcopy(self.internal)
        canaries = ['TOP_SECRET_TEST_ABC','SENSITIVE_ANSWER_123','PRIVATE_HTTPS_DASHBOARD']
        for item in private['opportunities']:
            item['description'] = canaries[0]
            item['requirements']['reference_evidence'] = canaries[1]
            item['example_evidence_urls'] = ['https://example.org/'+canaries[2]]
            item['example_intents'] = [canaries[0]]
        output = publicize_opportunities(private, KEY)
        sinks = json.dumps(output) + issue_title(output['opportunities'][0]) + issue_body(output['opportunities'][0])
        for canary in canaries:
            self.assertNotIn(canary, sinks)

    def test_no_key_or_malformed_category_fails_closed(self):
        for secret in (None, '', 'short'):
            with self.assertRaises(ValueError):
                publicize_opportunities(self.internal, secret)
        bad = copy.deepcopy(self.internal)
        bad['opportunities'][0]['category_id'] = 'weather\n### leaked'
        with self.assertRaises(ValueError):
            publicize_opportunities(bad, KEY)

    def test_key_rotation_detected(self):
        with self.assertRaises(ValueError):
            validate_public_export(self.public, 'a-different-production-key-000000000000000000001')

    def test_cli_default_and_needs_are_safe(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'public.json'
            cmd = [sys.executable, str(ROOT/'scripts/evaluation_opportunities.py'),
                   '--profiles',str(ROOT/'examples/evaluation-profiles.example.json'),
                   '--snapshot',str(ROOT/'examples/evaluation-state.example.ndjson'),
                   '--now', '2026-10-11T10:00:00Z', '--output', str(target)]
            env = dict(os.environ, TELEGRAPH_BOUNTY_PUBLICATION_KEY=KEY)
            result = subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            data=json.loads(target.read_text(encoding='utf-8'))
            validate_public_export(data, KEY)
            needs = subprocess.run([sys.executable,str(ROOT/'tb'),'needs',str(target)],cwd=ROOT,env=env,capture_output=True,text=True)
            self.assertEqual(needs.returncode,0,needs.stderr)
            sinks = result.stdout+result.stderr+target.read_text(encoding='utf-8')+needs.stdout+needs.stderr
            for x in ('WEATHER_FORECAST_VERIFY','quality_review','material_stale','min_source_domains','example.org','source_domains','known_blocked_apps'):
                self.assertNotIn(x,sinks)
            missing = subprocess.run(cmd,cwd=ROOT,env={k:v for k,v in env.items() if k != 'TELEGRAPH_BOUNTY_PUBLICATION_KEY'},capture_output=True,text=True)
            self.assertNotEqual(missing.returncode,0)
            self.assertNotIn('WEATHER_FORECAST_VERIFY', missing.stderr)
            self.assertNotIn(KEY, missing.stderr)


if __name__ == '__main__':
    unittest.main()

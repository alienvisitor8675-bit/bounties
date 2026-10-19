#!/usr/bin/env python3
"""Mock GitHub transport: only keyed, authorized, public-triage publishing."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import sync_evaluation_issues as sync
from evaluation_opportunities import compile_opportunities, load_profiles, iso_time
from evaluation_publication import publicize_opportunities

KEY = 'test-publisher-secret-not-for-deployment-000000000001'


class GitHubSyncTests(unittest.TestCase):
    def setUp(self):
        profiles = load_profiles(ROOT / 'examples/evaluation-profiles.example.json')
        snap = ROOT / 'examples/evaluation-state.example.ndjson'
        private = compile_opportunities(profiles, snap, now=iso_time('2026-10-11T10:00:00Z'))
        self.data = publicize_opportunities(private, KEY)

    def run_sync(self, approved, existing_issue=None, key=KEY):
        with tempfile.TemporaryDirectory() as tmp:
            opportunity_file = Path(tmp) / 'public.json'
            approval_file = Path(tmp) / 'approved.json'
            opportunity_file.write_text(json.dumps(self.data))
            approval_file.write_text(json.dumps({'verified_by':'maintainer', 'approved_ids':approved}))
            calls = []

            def fake_gh(*args):
                calls.append(args)
                if args[:2] == ('issue', 'list'):
                    return json.dumps([existing_issue] if existing_issue else [])
                if args[:2] == ('issue', 'create'):
                    return 'https://github.com/test/test/issues/1'
                raise AssertionError(args)

            argv = ['sync', '--opportunities', str(opportunity_file), '--approvals', str(approval_file), '--repo', 'example/repo', '--apply', '--now', '2026-10-11T10:00:00Z']
            with patch.object(sys, 'argv', argv), patch.dict(os.environ, {'TELEGRAPH_BOUNTY_PUBLICATION_KEY': key}, clear=False), patch.object(sync, 'gh', side_effect=fake_gh), contextlib.redirect_stdout(io.StringIO()):
                sync.main()
            return calls

    def test_only_explicit_approvals_create_unfunded_triage(self):
        ident = self.data['opportunities'][0]['id']
        calls = self.run_sync([ident])
        create = [c for c in calls if c[:2] == ('issue', 'create')]
        self.assertEqual(len(create), 1)
        joined = ' '.join(str(z) for z in create[0])
        for item in ('status:triage','reward:unfunded','source:protocol',ident,'weather-intelligence'):
            self.assertIn(item, joined)
        self.assertNotIn('status:open', joined)
        for forbidden in ('WEATHER_FORECAST_VERIFY', 'material_stale', 'source_diversity',
                          'min_eligible_items', 'weather-wasm-v1', 'example.org', '0.70'):
            self.assertNotIn(forbidden, joined)

    def test_existing_issues_never_overwritten_or_duplicated(self):
        ident = self.data['opportunities'][0]['id']
        existing = {'number': 17, 'title': 'human revised', 'state':'OPEN', 'body': f'<!-- telegraph-eval-opportunity {ident} -->', 'labels':[{'name':'status:claimed'}]}
        calls = self.run_sync([ident], existing)
        self.assertFalse(any(x[:2] == ('issue','create') for x in calls))

    def test_unapproved_issues_never_created(self):
        calls = self.run_sync([])
        self.assertFalse(any(x[:2] == ('issue','create') for x in calls))

    def test_legacy_detailed_issue_blocks_publication(self):
        ident = self.data['opportunities'][0]['id']
        legacy = {'number':8, 'state':'OPEN', 'title':'old detailed gap', 'body':'<!-- telegraph-eval-opportunity evalgap-0123456789abcdef -->', 'labels':[]}
        with self.assertRaisesRegex(RuntimeError, 'legacy detailed'):
            self.run_sync([ident], legacy)

    def test_wrong_key_disallows_publication(self):
        with self.assertRaises(SystemExit):
            self.run_sync([self.data['opportunities'][0]['id']], key='different-high-entropy-secret-00000000000000001')


if __name__ == '__main__':
    unittest.main()

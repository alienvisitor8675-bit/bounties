import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositorySecurity(unittest.TestCase):
    def test_main_ruleset_requires_independent_review_and_blocks_rewrites(self):
        data = json.loads((ROOT / '.github/security/main-ruleset.json').read_text())
        self.assertEqual(data['enforcement'], 'active')
        self.assertEqual(data['conditions']['ref_name']['include'], ['refs/heads/main'])
        self.assertEqual(data['conditions']['ref_name']['exclude'], [])
        self.assertEqual(data['bypass_actors'], [])
        rules = {rule['type']: rule.get('parameters', {}) for rule in data['rules']}
        self.assertTrue({'deletion', 'non_fast_forward', 'required_linear_history'} <= rules.keys())
        review = rules['pull_request']
        self.assertGreaterEqual(review['required_approving_review_count'], 1)
        for key in ('dismiss_stale_reviews_on_push', 'require_code_owner_review',
                    'require_last_push_approval', 'required_review_thread_resolution'):
            self.assertTrue(review[key])
        checks = rules['required_status_checks']
        self.assertTrue(checks['strict_required_status_checks_policy'])
        self.assertEqual({check['context'] for check in checks['required_status_checks']}, {
            'validate (ubuntu-latest, py3.10)', 'validate (ubuntu-latest, py3.13)',
            'validate (windows-latest, py3.13)', 'lint', 'analyze (javascript-typescript)',
            'analyze (python)', 'analyze (actions)',
        })
        self.assertTrue(all(check['integration_id'] == 15368 for check in checks['required_status_checks']))

    def test_release_tags_are_restricted_to_admins(self):
        data = json.loads((ROOT / '.github/security/release-ruleset.json').read_text())
        self.assertEqual(data['target'], 'tag')
        self.assertEqual(data['enforcement'], 'active')
        self.assertEqual(data['conditions']['ref_name'], {'include': ['refs/tags/v*'], 'exclude': []})
        self.assertEqual({rule['type'] for rule in data['rules']}, {'creation', 'update', 'deletion'})
        self.assertEqual(data['bypass_actors'], [{'actor_id': 5, 'actor_type': 'RepositoryRole', 'bypass_mode': 'always'}])

    def test_mutating_workflows_share_non_canceling_bounded_queue(self):
        for name in ('bounty-commands.yml', 'stale-claims.yml'):
            text = (ROOT / '.github/workflows' / name).read_text()
            self.assertIn('group: bounty-state-${{ github.repository }}', text)
            self.assertIn('cancel-in-progress: false', text)
            self.assertEqual(re.findall(r'^\s*queue:\s*(\S+)\s*$', text, re.M), ['max'])
            self.assertIn('persist-credentials: false', text)
        commands = (ROOT / '.github/workflows/bounty-commands.yml').read_text()
        self.assertIn("github.event.comment.user.type == 'User'", commands)
        self.assertIn('github.event.issue.pull_request == null', commands)
        self.assertNotIn('${{ github.event.comment.body }}', commands)


if __name__ == '__main__':
    unittest.main()

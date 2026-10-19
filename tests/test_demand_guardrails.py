import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DemandGuardrails(unittest.TestCase):
    def test_new_forms_start_in_triage_without_fake_source_or_reward(self):
        for name in ('capability-demand.yml', 'provider-opportunity.yml'):
            body = (ROOT / '.github/ISSUE_TEMPLATE' / name).read_text(encoding='utf-8')
            self.assertIn('status:triage', body)
            self.assertNotIn('source:customer', body)
            self.assertNotIn('reward:funded', body)
            self.assertIn('required: true', body)

    def test_provider_opportunity_excludes_bounty_automation(self):
        script = (ROOT / 'scripts/bounty_commands.js').read_text(encoding='utf-8')
        self.assertIn("labelNames().includes('opportunity:provider')", script)
        self.assertIn("'/claim'", script)
        self.assertIn("'/submit'", script)
        self.assertIn("'/approve'", script)

    def test_no_public_customer_ingestion_is_claimed(self):
        content = (ROOT / 'docs/DEMAND_INTAKE.md').read_text(encoding='utf-8')
        self.assertIn('does not expose an ingestion API', content)
        self.assertIn('consent', content.lower())
        self.assertIn('production system', content.lower())
        self.assertIn('private', content.lower())

    def test_existing_h2_and_evaluation_guards_retained(self):
        self.assertTrue((ROOT / 'seed/h2-bounties.json').exists())
        self.assertTrue((ROOT / 'scripts/evaluation_publication.py').exists())
        self.assertTrue((ROOT / 'tests/test_evaluation_publication_security.py').exists())


if __name__ == '__main__':
    unittest.main()

import importlib.util
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/launch_check.py'
spec=importlib.util.spec_from_file_location('launch_check',SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def issue(i, labels, body='## Reward\nNo monetary reward committed.'):
    return {'number':i,'labels':[{'name':x} for x in labels],'body':body}


class LiveLaunchTests(unittest.TestCase):
    def test_mixed_sources_count_as_permanent_board(self):
        items=[issue(i,['status:open','reward:unfunded',src]+(['priority:p0'] if i<3 else ['priority:p2'])+(['good first bounty'] if i>=4 else [])) for i,src in enumerate(['source:customer','source:mainnet','source:release','source:h2','source:customer'],1)]
        self.assertEqual([],mod.validate_live(items))

    def test_provider_leads_and_triage_do_not_count(self):
        items=[issue(i,['status:open','priority:p0','good first bounty','opportunity:provider']) for i in range(7)]
        items.append(issue(9,['status:triage','priority:p0','good first bounty']))
        self.assertTrue(mod.validate_live(items))

    def test_funded_issue_needs_real_terms(self):
        base=[issue(i,['status:open','priority:p0','good first bounty']) for i in range(1,6)]
        base[0]=issue(1,['status:open','priority:p0','good first bounty','reward:funded'],'## Reward\nReward announced soon')
        self.assertTrue(any('missing' in e for e in mod.validate_live(base)))


if __name__=='__main__': unittest.main()

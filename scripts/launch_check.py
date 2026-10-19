#!/usr/bin/env python3
"""Announcement data gates for approved local H2 seed or actual live public board.

This validates visible work, not production readiness or customer demand.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def validate_live(issues):
    # Commercial Provider recruitment is not a claimable bounty and is excluded.
    active=[]
    errors=[]
    for issue in issues:
        names={v['name'] if isinstance(v,dict) else v for v in issue.get('labels',[])}
        if 'status:open' not in names or 'opportunity:provider' in names:
            continue
        active.append((issue,names))
        if 'reward:funded' in names:
            body=issue.get('body','') or ''
            section=re.search(r'^## Reward\s*\n([\s\S]*?)(?=^##\s|\Z)',body,re.M)
            terms=section.group(1) if section else ''
            for field in ['Amount:', 'Payout asset:', 'Eligibility:', 'Verification:', 'Payout window:']:
                if field not in terms:
                    errors.append(f"Funded Issue #{issue.get('number','?')} missing {field}")
            if re.search(r'^-\s*Conversion rule:',terms,re.M) is None and re.search(r'\bUSD\b',terms) and re.search(r'\bMACHINA\b',terms):
                errors.append(f"Funded Issue #{issue.get('number','?')} has no cross-asset conversion rule")
    if len(active)<5: errors.append(f'need at least 5 real open claimable bounties; found {len(active)}')
    if sum(bool({'priority:p0','priority:p1'} & labels) for _,labels in active)<2:
        errors.append('need at least 2 P0/P1 open claimable bounties')
    if sum('good first bounty' in labels for _,labels in active)<2:
        errors.append('need at least 2 open good-first-bounty tasks')
    return errors


def get_live_issues():
    repo=subprocess.check_output(['gh','repo','view','--json','nameWithOwner','-q','.nameWithOwner'],cwd=ROOT,text=True).strip()
    # GitHub REST pagination through gh api avoids a misleading first-page-only check.
    raw=subprocess.check_output(['gh','api',f'repos/{repo}/issues','--method','GET','--paginate','-f','state=open','-f','per_page=100'],cwd=ROOT,text=True)
    decoder=json.JSONDecoder()
    items=[]
    while raw.strip():
        raw=raw.lstrip()
        item,end=decoder.raw_decode(raw)
        if not isinstance(item,list): raise ValueError('Unexpected issues API shape')
        items.extend(x for x in item if 'pull_request' not in x)
        raw=raw[end:]
    return items


def validate_seed():
    errors=[]
    for required in ['README.md','LICENSE','SECURITY.md','CONTRIBUTING.md','AGENTS.md','catalog/intents.json','catalog/missions.json','assets/social-preview.png']:
        if not (ROOT/required).exists(): errors.append(f'missing {required}')
    security=(ROOT/'SECURITY.md').read_text(encoding='utf-8') if (ROOT/'SECURITY.md').exists() else ''
    if 'info@telegraphprotocol.com' not in security: errors.append('SECURITY.md has no private contact')
    seed=json.loads((ROOT/'seed/h2-bounties.json').read_text(encoding='utf-8'))
    pub=[x for x in seed if x.get('publish')]
    if len(pub)<5: errors.append(f'need at least 5 approved publish=true launch bounties; have {len(pub)}')
    if sum(x.get('priority') in ('p0','p1') for x in pub)<2: errors.append('need at least 2 P0/P1 launch bounties')
    if sum(bool(x.get('good_first_bounty')) for x in pub)<2: errors.append('need at least 2 good-first-bounty launch items')
    for x in pub:
        reward=x.get('reward',{})
        if reward.get('funded'):
            fields=['amount','denomination','payout_asset','eligibility','verification_condition','payout_window']
            missing=[f for f in fields if reward.get(f) in (None,'')]
            if missing: errors.append(f"funded bounty missing reward fields {missing}: {x['title']}")
    return errors


def main():
    if '--live' in sys.argv:
        try:
            errors=validate_live(get_live_issues())
        except (FileNotFoundError,subprocess.CalledProcessError,ValueError) as exc:
            print(f'LIVE BOARD NOT VERIFIED: authenticate GitHub CLI and select the correct repository: {exc}')
            return 1
    else:
        errors=validate_seed()
    if errors:
        print('NOT ANNOUNCEMENT-READY:')
        for e in errors:print(' -',e)
        return 1
    print('ANNOUNCEMENT DATA GATE PASSED. Manually verify real work, privacy, rewards and production readiness before public launch.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())

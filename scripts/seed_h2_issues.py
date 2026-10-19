#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'seed/h2-bounties.json').read_text(encoding='utf-8'))

def sh(*args, check=True):
    p=subprocess.run(args,text=True,capture_output=True)
    if check and p.returncode:
        print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
    return p.stdout.strip()

sh('gh','auth','status')
repo=sh('gh','repo','view','--json','nameWithOwner','-q','.nameWithOwner')

for item in DATA:
    if not item.get('publish'): continue
    title=item['title']
    existing=sh('gh','issue','list','--repo',repo,'--state','all','--search',f'"{title}" in:title','--json','title','--jq','.[].title',check=False)
    if title in existing.splitlines():
        print(f'skip existing: {title}'); continue
    labels=[f"work:{item['work_type']}",f"priority:{item['priority']}",'source:h2','status:open','help wanted']
    if item.get('gap_type'): labels.append(f"gap:{item['gap_type']}")
    labels.extend(f"mission:{m}" for m in item.get('missions',[]))
    if item.get('good_first_bounty'): labels.append('good first bounty')
    reward=item.get('reward',{})
    labels.append('reward:funded' if reward.get('funded') else 'reward:unfunded')

    body=[]
    if item.get('intent'): body += [f"## Intent\n`{item['intent']}`\n"]
    body += [f"## Why this matters\n{item['why']}\n"]
    if item.get('missions'):
        body += ['## Demand / mission impact\n'+'\n'.join(f'- `{m}`' for m in item['missions'])+'\n']
    if item.get('current_state'): body += [f"## Current state\n{item['current_state']}\n"]
    body += ['## Acceptance criteria\n'+'\n'.join(f'- [ ] {x}' for x in item['acceptance'])+'\n']
    if reward.get('funded'):
        conversion = reward.get('conversion_rule')
        body += ["## Reward\n"+
                 f"- Amount: **{reward['amount']} {reward['denomination']}**\n"+
                 f"- Payout asset: **{reward['payout_asset']}**\n"+
                 (f"- Conversion rule: {conversion}\n" if conversion else "")+
                 "- Max awards: **1** (one claimant/award per Issue; create separate slot Issues for additional independent implementations)\n"+
                 f"- Eligibility: {reward['eligibility']}\n"+
                 f"- Verification: {reward['verification_condition']}\n"+
                 f"- Payout window: {reward['payout_window']}\n"+
                 "- Claim-time lock: reward terms are snapshotted by the bot when `/claim` succeeds.\n"]
    else:
        body += ['## Reward\nNo monetary/token reward is currently committed. This issue may still carry H2 eligibility/recognition only if explicitly stated elsewhere.\n']
    body += ['## Claim / submit\nComment `/claim` to coordinate work. Post `/progress ...` at least every 72 hours. When complete, comment `/submit ...` with repository/demo/evidence links.\n']
    metadata={k:item.get(k) for k in ['intent','work_type','gap_type','priority','missions','reward']}
    body += ['<!-- telegraph-bounty\n'+json.dumps(metadata,separators=(',',':'))+'\n-->\n']
    cmd=['gh','issue','create','--repo',repo,'--title',title,'--body','\n'.join(body)]
    for label in labels: cmd += ['--label',label]
    print('created:', sh(*cmd))

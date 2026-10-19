#!/usr/bin/env python3
import json, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
INTENTS = json.loads((ROOT/'catalog/intents.json').read_text(encoding='utf-8'))
MISSIONS = json.loads((ROOT/'catalog/missions.json').read_text(encoding='utf-8'))
mission_name = {m['id']: m['name'] for m in MISSIONS}


def render_intents():
    by_cat = defaultdict(list)
    for x in INTENTS:
        by_cat[x['category']].append(x)
    out = [
        '# Intent Catalogue', '',
        f'**{len(INTENTS)} reusable machine-intelligence capabilities.**', '',
        'This is the public H2 catalogue used by Telegraph Bounties. Intents are reusable intelligence markets; missions may compose several of them.', '',
        '> Mission usage is a starting coordination map, not a restriction. Apps may use any relevant Intent.', '',
        "> **Important:** `evaluation_mechanism` and `scoring_path` are H2/reference coordination metadata. They are **not** immutable Canonical Evaluators or permanent protocol state. Telegraph's live Canonical Evaluator for an Intent is determined by the protocol's competitive Evaluator-selection and verification process and may change over time.", ''
    ]
    for cat in sorted(by_cat):
        out += [f'## {cat}', '', '| Intent | Tier | Class | Latency | Used by H2 missions |', '|---|---|---|---|---|']
        for x in sorted(by_cat[cat], key=lambda i:(-int(i['priority_score']), i['name'])):
            used = ', '.join(mission_name[mid] for mid in x.get('used_by_missions', [])) or '—'
            out.append(f"| `{x['name']}` | {x['tier']} | {x['class']} | {x.get('target_latency') or '—'} | {used} |")
        out += ['', '### Details', '']
        for x in sorted(by_cat[cat], key=lambda i:(-int(i['priority_score']), i['name'])):
            out += [f"#### `{x['name']}`", '', x['description'], '']
            bits = [f"Priority: **{x['priority_score']}**", f"Scoring path: `{x.get('scoring_path') or '—'}`", f"Verification complexity: **{x.get('verification_complexity') or '—'}**"]
            if x.get('evaluation_mechanism'):
                bits.append(f"Evaluation: `{x['evaluation_mechanism']}`")
            out += [' · '.join(bits), '']
    return '\n'.join(out).rstrip()+'\n'


def render_missions():
    out = ['# Season II Mission → Intent Map', '', '**15 commercial missions define the end states. Reusable Intents provide the intelligence underneath them.**', '',
           'Apps build for missions. Miners and Evaluators build for Intents. The same Intent can power many missions.', '']
    for i,m in enumerate(MISSIONS,1):
        out += [f"## {i:02d}. {m['name']}", '', 'Core starting Intents:', '']
        out += [f"- `{x}`" for x in m['core_intents']]
        out += ['', '> This map is a coordination baseline, not a hard whitelist. App builders may compose any relevant Telegraph Intents.', '']
    return '\n'.join(out).rstrip()+'\n'


def render_network_map():
    usage = sorted(((x['name'], x.get('used_by_missions', [])) for x in INTENTS), key=lambda p:(-len(p[1]), p[0]))
    out=['# H2 Intent Coverage & Reuse Map','', 'Which reusable Intents appear across the most Season II missions?', '', '> Mission reuse is **not** market demand. This map only shows how often an Intent appears in the starting H2 mission design.', '', '| Intent | H2 mission count | Missions |', '|---|---:|---|']
    for name,mids in usage:
        if not mids: continue
        out.append(f"| `{name}` | {len(mids)} | {', '.join(mission_name[m] for m in mids)} |")
    out += ['', 'This is **not** a demand score or readiness score. It only shows reuse across the starting mission map. Live demand/readiness belongs in actual usage evidence and GitHub Issues / bounties.', '']
    return '\n'.join(out).rstrip()+'\n'

outputs = {
    ROOT/'docs/INTENTS.md': render_intents(),
    ROOT/'docs/MISSIONS.md': render_missions(),
    ROOT/'docs/NETWORK_MAP.md': render_network_map(),
}

check='--check' in sys.argv
failed=False
for path,content in outputs.items():
    if check:
        if not path.exists() or path.read_text(encoding='utf-8')!=content:
            print(f'OUT OF DATE: {path.relative_to(ROOT)}')
            failed=True
    else:
        path.write_text(content,encoding='utf-8',newline='\n')
        print(f'wrote {path.relative_to(ROOT)}')
if failed: raise SystemExit(1)

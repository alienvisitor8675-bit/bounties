#!/usr/bin/env python3
"""Review/publish strictly sanitized Category-level evaluation opportunities.

All public bodies, titles and console output use an explicit allowlist. Only a
trusted internal indexer may calculate per-Intent diagnostics. Issue creation
is opt-in, requires key-bound public IDs and maintainer approval, and makes
only unfunded triage issues. Never writes or reads hidden qualification material.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path

from evaluation_publication import validate_public_export
from evaluation_opportunities import iso_time

MARKER = re.compile(r'<!-- telegraph-eval-opportunity (evalpub-[a-f0-9]{24}) -->')
LEGACY_MARKER = re.compile(r'<!-- telegraph-eval-opportunity evalgap-[a-f0-9]{16} -->')


def check_result(data, now, max_hours, secret=None):
    issues = validate_public_export(data, secret)
    age = (now - iso_time(data['generated_at'])).total_seconds() / 3600
    if age < -1 or age > max_hours:
        raise ValueError('public opportunity export expired or future-dated')
    return issues


def issue_title(item):
    return f"[Evaluation][{item['category_id']}] Evaluation contributions"


def issue_body(item):
    # item must be validated before rendering. Every character below is either
    # literal or a schema-restricted public Category or keyed opaque ID.
    return f'''## Public contribution opportunity
Category: `{item['category_id']}`

Telegraph welcomes Category-compatible evaluation methods, independently supported references, task examples, and scoring improvements. Compatible specialized Intents may share scoring logic, but qualification and Miner Rankings remain per Intent under V2.

## How to contribute
- Follow the **public** Category documentation and the existing V2 contribution interface. Use independently supportable evidence where possible.
- Submit the method/material and non-sensitive reproducibility information through the approved contribution workflow.
- Demonstrate general task compatibility and an independently assessable quality improvement where feasible. No Miner should be predetermined to win.
- Maintainers will privately scope and validate work against live requirements before this opportunity becomes a claimable, funded bounty.

**No exact coverage gaps, per-Intent weaknesses, source statistics, hidden tests, or qualification thresholds are disclosed here.** Do not post these details, customer payloads, credentials, security flaws or sensitive test cases in public Issues or comments. For sensitive reports, see SECURITY.md.

## Review and funding
- [ ] Maintainer confirms safe public acceptance criteria and a legitimate need.
- [ ] Maintainer confirms authorized testing and review path.
- [ ] Any bounty reward and claimable status require separate explicit approval under the existing workflow.

This starts at `status:triage` and is not claimable until a maintainer uses `/open`. No monetary/token bounty is promised. V2 Evaluator emissions are independent, demand-backed and not earned just by opening an Issue.

<!-- telegraph-eval-opportunity {item['id']} -->
'''


def gh(*args):
    r = subprocess.run(('gh', *map(str, args)), capture_output=True, text=True)
    if r.returncode:
        # Do not echo upstream error text: it may contain secrets or internal logs.
        raise RuntimeError('GitHub CLI action failed; inspect local authorized diagnostics')
    return r.stdout.strip()


def existing_issues(repo):
    items = json.loads(gh('issue', 'list', '--repo', repo, '--state', 'all', '--label', 'source:protocol', '--limit', '1000', '--json', 'number,title,body,state,labels'))
    if len(items) >= 1000:
        raise RuntimeError('Issue list may be incomplete; refusing to create duplicates')
    seen = {}
    for issue in items:
        if LEGACY_MARKER.search(issue.get('body') or ''):
            raise RuntimeError('legacy detailed evaluation Issue found; review/redact manually before publishing any new evaluation opportunities')
        match = MARKER.search(issue.get('body') or '')
        if match:
            if match.group(1) in seen:
                raise RuntimeError('duplicate public evaluation opportunity IDs')
            seen[match.group(1)] = issue
    return seen


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--opportunities', required=True, help='public projection only, never internal state')
    a.add_argument('--apply', action='store_true', help='create approved unfunded triage issues')
    a.add_argument('--approvals', help='JSON: approved_ids, verified_by')
    a.add_argument('--repo', help='GitHub owner/repo (required with --apply)')
    a.add_argument('--max-opportunity-hours', type=float, default=24)
    a.add_argument('--now', help='test-only UTC ISO timestamp')
    args = a.parse_args()
    now = iso_time(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    if args.max_opportunity_hours <= 0:
        a.error('max-opportunity-hours must be positive')
    if args.apply and (not args.repo or '/' not in args.repo or not args.approvals):
        a.error('--apply requires --repo owner/repo and --approvals')
    secret = os.getenv('TELEGRAPH_BOUNTY_PUBLICATION_KEY') if args.apply else None
    if args.apply and not secret:
        a.error('authorized publication key required for --apply')
    # Reject internal exports/unknown fields BEFORE any external API calls.
    try:
        items = check_result(json.loads(Path(args.opportunities).read_text(encoding='utf-8')), now, args.max_opportunity_hours, secret)
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        a.error('invalid, expired or non-public opportunity export')
    approved = set()
    if args.approvals:
        try:
            signed = json.loads(Path(args.approvals).read_text(encoding='utf-8'))
            if not isinstance(signed, dict) or set(signed) != {'approved_ids', 'verified_by'} or not isinstance(signed['approved_ids'], list) or not isinstance(signed['verified_by'], str) or not signed['verified_by'].strip():
                raise ValueError('invalid approval schema')
            if not all(isinstance(x, str) for x in signed['approved_ids']):
                raise ValueError('invalid approval IDs')
            approved = set(signed['approved_ids'])
            if len(approved) != len(signed['approved_ids']) or approved - {x['id'] for x in items}:
                raise ValueError('unknown or duplicate approval IDs')
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            a.error('invalid approval authorization; review locally')
    live = existing_issues(args.repo) if args.apply else {}
    for item in items:
        key = item['id']
        status = 'EXISTING (unchanged)' if key in live else 'APPROVED FOR TRIAGE' if key in approved else 'REVIEW ONLY'
        print(f'{key}: {status}: {issue_title(item)}')
        if args.apply and key in approved and key not in live:
            labels = ['work:evaluator', 'gap:evaluation', 'source:protocol', 'status:triage', 'help wanted', 'reward:unfunded']
            cmd = ['issue', 'create', '--repo', args.repo, '--title', issue_title(item), '--body', issue_body(item)]
            for label in labels:
                cmd += ['--label', label]
            print('  Created:', gh(*cmd))
    if args.apply and set(live) - {x['id'] for x in items}:
        print('Some existing public opportunities were not present; review privately. No issue was changed.')


if __name__ == '__main__':
    main()

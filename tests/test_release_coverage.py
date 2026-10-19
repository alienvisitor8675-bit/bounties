#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

form = (ROOT/'.github/ISSUE_TEMPLATE/release-coverage.yml').read_text(encoding='utf-8')
doc = (ROOT/'docs/RELEASE_COVERAGE.md').read_text(encoding='utf-8')
bootstrap = (ROOT/'scripts/bootstrap_github.sh').read_text(encoding='utf-8')
agents = (ROOT/'AGENTS.md').read_text(encoding='utf-8')
h2 = (ROOT/'docs/H2.md').read_text(encoding='utf-8')

assert 'source:release' in form
assert 'Canonical release source' in form
assert 'Do not require a particular rank or winner' in form
assert 'source:release' in bootstrap
assert 'never require a predetermined rank' in agents
assert 'does **not** impose one universal response schema' in h2
assert 'fair eligibility' in doc
assert 'not on winning' in doc
assert 'Do **not** invent customer demand' in doc
assert 'Provider-native interfaces may differ' in doc

print('RELEASE COVERAGE OK')

assert 'Historical receipt vs current status' in doc
assert 'Never let an old `#1` event receipt silently present itself' in doc

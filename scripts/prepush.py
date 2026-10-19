#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd):
    subprocess.run(cmd, cwd=ROOT, check=True)


checks = [
    [sys.executable, str(ROOT / 'scripts/validate_catalog.py')],
    [sys.executable, str(ROOT / 'scripts/generate_docs.py'), '--check'],
    ['node', '--check', str(ROOT / 'scripts/bounty_state.js')],
    ['node', '--check', str(ROOT / 'scripts/bounty_commands.js')],
    ['node', '--check', str(ROOT / 'scripts/stale_claims.js')],
    ['node', str(ROOT / 'tests/test_bounty_workflow.js')],
    ['node', str(ROOT / 'tests/test_stale_claims.js')],
    [sys.executable, str(ROOT / 'tests/test_reward_validation.py')],
    [sys.executable, str(ROOT / 'tests/test_demand_guardrails.py')],
    [sys.executable, str(ROOT / 'tests/test_live_launch_check.py')],
    [sys.executable, str(ROOT / 'tests/test_release_coverage.py')],
    [sys.executable, str(ROOT / 'tests/test_evaluation_opportunities.py')],
    [sys.executable, str(ROOT / 'tests/test_evaluation_sync.py')],
    [sys.executable, str(ROOT / 'tests/test_evaluation_publication_security.py')],
]
for cmd in checks:
    run(cmd)

# Compile every maintained Python script rather than only the files reached above.
python_scripts = sorted((ROOT / 'scripts').glob('*.py'))
run([sys.executable, '-m', 'py_compile', *map(str, python_scripts)])

# Shell syntax is part of the launch surface as well.
for shell in sorted((ROOT / 'scripts').glob('*.sh')):
    run(['bash', '-n', str(shell)])

required = [
    'README.md', 'LICENSE', 'SECURITY.md', 'GOVERNANCE.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md',
    'docs/README.md', 'docs/GLOSSARY.md', 'docs/maintainers/README.md', 'docs/maintainers/LAUNCH.md', 'docs/maintainers/PUBLISH.md', 'docs/maintainers/REPO_SETTINGS.md',
    '.github/workflows/lint.yml', '.github/workflows/codeql.yml', '.github/dependabot.yml', 'pyproject.toml',
    '.gitattributes', '.editorconfig', 'package.json',
    '.github/workflows/bounty-commands.yml',
    '.github/workflows/stale-claims.yml',
    '.github/workflows/validate.yml',
    'scripts/bounty_state.js',
    'scripts/bounty_commands.js',
    'scripts/stale_claims.js',
    'tests/test_bounty_workflow.js',
    'tb',
    '.github/ISSUE_TEMPLATE/release-coverage.yml',
    'docs/RELEASE_COVERAGE.md',
    'docs/EVALUATION_NEEDS.md',
    'docs/DEMAND_INTAKE.md',
    '.github/ISSUE_TEMPLATE/capability-demand.yml',
    '.github/ISSUE_TEMPLATE/provider-opportunity.yml',
    '.github/ISSUE_TEMPLATE/evaluation-material-gap.yml',
    'scripts/evaluation_opportunities.py',
    'scripts/evaluation_publication.py',
    'scripts/sync_evaluation_issues.py',
]
for p in required:
    assert (ROOT / p).exists(), f'Missing {p}'

print('PREPUSH OK')

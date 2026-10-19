# GitHub repository settings checklist

Workflows and config files in this repo cannot enable these controls. A repository admin applies them once after the repo is created, then re-checks them before announcing it. Settings are under **Settings** unless noted.

## 1. Branch protection (Rules → Rulesets → New branch ruleset, target `main`)

- [ ] Restrict deletions and block force pushes
- [ ] Require a pull request before merging
  - [ ] Require at least 1 approval; dismiss stale approvals on new commits
  - [ ] Require approval of the most recent push by someone other than the pusher
  - [ ] Require review from Code Owners (once `CODEOWNERS` exists)
- [ ] Require status checks to pass, branches up to date. Required checks:
  - `validate (ubuntu-latest, py3.10)`
  - `validate (ubuntu-latest, py3.13)`
  - `validate (windows-latest, py3.13)`
  - `lint`
  - `analyze (javascript-typescript)`, `analyze (python)`, `analyze (actions)`
- [ ] Require linear history
- [ ] Require signed commits (optional)
- [ ] Do not allow bypass, including admins, except a named break-glass role

Check names must match the job names in `.github/workflows/`. If you rename a job, update this list.

## 2. Actions (Actions → General)

- [ ] Allow only actions created by GitHub, plus selected actions if you add any; require actions to be pinned to a full commit SHA
- [ ] Workflow permissions: **Read repository contents** (default); do not allow Actions to create or approve pull requests
- [ ] Fork pull requests: **require approval for all outside collaborators**
- [ ] Send write tokens or secrets to fork PR workflows: **off**

The bounty-command workflow runs on `issue_comment` with `issues: write`, so keep these restrictions on.

## 3. Code security (Settings → Advanced Security)

- [ ] Dependency graph and Dependabot alerts
- [ ] Dependabot security updates (version updates come from `.github/dependabot.yml`)
- [ ] Secret scanning and **push protection**
- [ ] Private vulnerability reporting (the Security tab path named in `SECURITY.md`)
- [ ] Code scanning: CodeQL runs from `.github/workflows/codeql.yml`; do not also enable default setup

## 4. Access

- [ ] Base permission for members: **Read**
- [ ] Maintainers hold **Write** or higher through a team, not individual grants. Anyone with Write can run `/open`, `/approve` and `/release`; review the list regularly
- [ ] Two or more admins; no shared accounts
- [ ] Require two-factor authentication for the organisation

## 5. Secrets and environments

- [ ] No repository secrets are needed for the workflows in this repo
- [ ] `TELEGRAPH_BOUNTY_PUBLICATION_KEY` lives only in the operator's protected secret store, never in repository or organisation secrets accessible to pull requests
- [ ] Raw evaluation snapshots and profiles are never committed or attached to workflow runs

## 6. Labels, features and discovery

- [ ] Run `bash scripts/bootstrap_github.sh` (labels, topics, description, Discussions)
- [ ] Disable Wiki
- [ ] Upload `assets/social-preview.png` (Settings → Social preview)
- [ ] Pin the repository on the organisation profile

## 7. Dry run before announcing

- [ ] On a disposable Issue, test `/open`, `/claim`, `/progress`, `/submit`, `/changes`, `/approve`, `/release`
- [ ] Confirm a non-maintainer cannot run `/open`, `/approve` or `/changes`
- [ ] Confirm `opportunity:provider` Issues reject `/claim`
- [ ] Open a test PR and confirm every required check runs and blocks merge on failure

# GitHub repository settings checklist

A repository admin applies these server-side controls after creation and verifies them before announcement. Repository workflows and configuration files cover the corresponding code-level controls. Settings are under **Settings** unless noted.

Importable examples are in `.github/security/main-ruleset.json` and
`.github/security/release-ruleset.json`. Confirm the configured code owners can
provide independent human review before enforcing it. See [FUNDED_LAUNCH.md](FUNDED_LAUNCH.md)
for deployment verification, treasury separation and the funded-launch gate.

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
- [ ] Limit bypass to a named break-glass role; administrators follow the ruleset

Check names must match the job names in `.github/workflows/`. If you rename a job, update this list.

## 2. Actions (Actions → General)

- [ ] Allow GitHub-authored and explicitly selected actions; pin every external action to a full commit SHA
- [ ] Workflow permissions: **Read repository contents** (default); leave pull-request creation and approval disabled
- [ ] Fork pull requests: **require approval for all outside collaborators**
- [ ] Send write tokens or secrets to fork PR workflows: **off**

The bounty-command workflow runs on `issue_comment` with `issues: write`, so keep these restrictions on.

## 3. Code security (Settings → Advanced Security)

- [ ] Dependency graph and Dependabot alerts
- [ ] Dependabot security updates (version updates come from `.github/dependabot.yml`)
- [ ] Secret scanning and **push protection**
- [ ] Private vulnerability reporting (the Security tab path named in `SECURITY.md`)
- [ ] Code scanning: use `.github/workflows/codeql.yml` and leave CodeQL default setup disabled

## 4. Access

- [ ] Base permission for members: **Read**
- [ ] Maintainers receive **Write** or higher through a team. Anyone with Write can run `/open`, `/approve` and `/release`; review membership regularly
- [ ] Two or more admins, each using an individual account
- [ ] Require two-factor authentication for privileged accounts; use organization enforcement when organization-owned
- [ ] Use passkeys or hardware security keys for privileged accounts; test recovery
- [ ] Separate work review and treasury signing; approval comes from someone other than the claimant and submitter

## 5. Secrets and environments

- [ ] Keep repository secrets empty for the workflows in this repository
- [ ] Store `TELEGRAPH_BOUNTY_PUBLICATION_KEY` in the operator's protected secret store, outside secrets available to repository pull requests
- [ ] Keep raw evaluation snapshots and profiles out of commits and workflow artifacts

## 6. Labels, features and discovery

- [ ] Run `bash scripts/bootstrap_github.sh` (labels, topics, description, Discussions)
- [ ] Disable Wiki
- [ ] Upload `assets/social-preview.png` (Settings → Social preview)
- [ ] Pin the repository on the organisation profile

## 7. Dry run before announcing

- [ ] On a disposable Issue, test `/open`, `/claim`, `/progress`, `/submit`, `/changes`, `/approve`, `/release`
- [ ] Confirm `/open`, `/approve` and `/changes` reject users without maintainer permission
- [ ] Confirm `opportunity:provider` Issues reject `/claim`
- [ ] Open a test PR and confirm every required check runs and blocks merge on failure

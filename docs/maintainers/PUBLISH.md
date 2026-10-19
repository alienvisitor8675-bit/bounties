# Publish the repository

Everything can be prepared locally. The only account-specific step is GitHub authentication/authorization.

## One-command path

```bash
gh auth login
./scripts/publish_repo.sh <YOUR_GITHUB_ORG>
```

The script:

1. runs the pre-push checks;
2. requires the local branch to be `main`;
3. creates (or safely reuses) `telegraph-bounties`;
4. pushes the repository;
5. creates the labels/topics/settings with `make bootstrap`.

It will **not** overwrite an unrelated existing repository.

## Then

1. audit actual live H2 readiness;
2. put only real gaps in `seed/h2-bounties.json`;
3. set approved entries to `"publish": true`;
4. define reward terms where funded;
5. run `make seed-h2`;
6. run `make launch-check` for the initial offline H2 seed, or `make launch-check-live` once the actual ongoing/H2 Issues are live;
7. review non-H2 customer/mainnet contribution needs independently of H2 and confirm public-safe scope;
8. upload `assets/social-preview.png` in GitHub repository settings;
9. pin the repo and announce it.

Pushing and announcing are intentionally separate. The repository may be structurally ready while the public bounty queue is not yet populated.

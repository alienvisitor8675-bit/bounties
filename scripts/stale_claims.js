'use strict';

const {
  parseState,
  isStaleWarningFor,
} = require('./bounty_state');

module.exports = async function runStaleClaims({ github, context }) {
  const owner = context.repo.owner;
  const repo = context.repo.repo;
  const issues = await github.paginate(github.rest.issues.listForRepo, {
    owner, repo, state: 'open', labels: 'status:claimed', per_page: 100,
  });

  for (const issue of issues) {
    if (issue.pull_request) continue;
    let comments = await github.paginate(github.rest.issues.listComments, {
      owner, repo, issue_number: issue.number, per_page: 100,
    });
    let state = parseState(comments);
    if (!state.claimant || !state.lastProgressAt) continue;

    let ageHours = (Date.now() - new Date(state.lastProgressAt).getTime()) / 36e5;
    const alreadyWarned = comments.some(c => isStaleWarningFor(c, state.claimant, state.claimedAt));

    if (ageHours >= 72) {
      // Re-read immediately before mutation so a just-posted /progress or manual release is observed.
      comments = await github.paginate(github.rest.issues.listComments, {
        owner, repo, issue_number: issue.number, per_page: 100,
      });
      state = parseState(comments);
      if (!state.claimant || !state.lastProgressAt) continue;
      ageHours = (Date.now() - new Date(state.lastProgressAt).getTime()) / 36e5;
      if (ageHours < 72) continue;

      const latestIssue = (await github.rest.issues.get({ owner, repo, issue_number: issue.number })).data;
      const labels = latestIssue.labels.map(l => typeof l === 'string' ? l : l.name);
      if (!labels.includes('status:claimed')) continue;
      const nextLabels = labels.filter(l => l !== 'status:claimed' && l !== 'status:open');
      nextLabels.push('status:open');
      await github.rest.issues.setLabels({ owner, repo, issue_number: issue.number, labels: nextLabels });
      const now = new Date().toISOString();
      await github.rest.issues.createComment({
        owner, repo, issue_number: issue.number,
        body: `<!-- telegraph-release user="telegraph-bot" at="${now}" -->\n@${state.claimant}'s claim was automatically released after **72 hours without a \`/progress\` update**. This bounty is open again.`,
      });
    } else if (ageHours >= 48 && !alreadyWarned) {
      await github.rest.issues.createComment({
        owner, repo, issue_number: issue.number,
        body: `<!-- telegraph-stale-warning claimant="${state.claimant}" claimed_at="${state.claimedAt}" -->\n@${state.claimant}: this claim has had no \`/progress\` update for 48 hours. Post an update before 72 hours to keep the claim.`,
      });
    }
  }
};

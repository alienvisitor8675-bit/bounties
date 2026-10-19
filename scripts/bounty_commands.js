'use strict';

const {
  parseState,
  snapshotReward,
  quoteMarkdown,
  permissionAllowsMaintenance,
} = require('./bounty_state');

const STATUS_LABELS = [
  'status:triage', 'status:open', 'status:claimed',
  'status:review', 'status:blocked', 'status:done',
];

module.exports = async function runBountyCommand({ github, context }) {
  const raw = String(context.payload.comment.body || '').trim();
  if (!raw.startsWith('/')) return;

  const [command, ...rest] = raw.split(/\s+/);
  const payload = rest.join(' ').trim();
  const owner = context.repo.owner;
  const repo = context.repo.repo;
  const issue_number = context.issue.number;
  const actor = context.actor;

  const issueResp = await github.rest.issues.get({ owner, repo, issue_number });
  let issue = issueResp.data;
  const labelNames = () => issue.labels.map(l => typeof l === 'string' ? l : l.name);

  async function refresh() {
    issue = (await github.rest.issues.get({ owner, repo, issue_number })).data;
  }
  async function setStatus(name) {
    const labels = labelNames().filter(label => !STATUS_LABELS.includes(label));
    labels.push(name);
    await github.rest.issues.setLabels({ owner, repo, issue_number, labels });
    await refresh();
  }
  async function comment(body) {
    await github.rest.issues.createComment({ owner, repo, issue_number, body });
  }
  async function comments() {
    return github.paginate(github.rest.issues.listComments, { owner, repo, issue_number, per_page: 100 });
  }

  let maintainerPermission;
  async function isMaintainer() {
    if (maintainerPermission !== undefined) return maintainerPermission;
    try {
      const resp = await github.rest.repos.getCollaboratorPermissionLevel({ owner, repo, username: actor });
      maintainerPermission = permissionAllowsMaintenance(resp.data?.permission);
    } catch (_) {
      maintainerPermission = false;
    }
    return maintainerPermission;
  }

  // An approved Provider recruitment listing is not a development bounty or an award.
  // Do not let either ordinary contributors or maintainer overrides use the bounty claim/submit lifecycle.
  if (labelNames().includes('opportunity:provider') &&
      ['/claim', '/progress', '/release', '/submit', '/changes', '/approve'].includes(command)) {
    await comment('This is a commercial Provider onboarding opportunity, not a claimable GitHub bounty. Please follow its public contact instructions; onboarding and any terms are coordinated separately.');
    return;
  }

  const all = await comments();
  const state = parseState(all);
  const now = new Date().toISOString();

  if (command === '/claim') {
    if (!labelNames().includes('status:open')) {
      await comment('This Issue is not currently open for claiming. Only `status:open` bounties can be claimed.');
      return;
    }
    if (state.claimant) {
      await comment(`Already claimed by @${state.claimant}. If the claim is stale, a maintainer can release it.`);
      return;
    }

    const reward = snapshotReward(issue.body);
    const rewardHash = reward.sha256 || 'none';
    const rewardText = reward.text
      ? `\n\n**Reward terms locked for this claim** (SHA-256 \`${rewardHash}\`):\n${quoteMarkdown(reward.text)}`
      : '\n\n**Reward terms locked for this claim:** no explicit `## Reward` section was present at claim time.';

    await setStatus('status:claimed');
    await comment(
      `<!-- telegraph-claim user="${actor}" at="${now}" reward_sha256="${rewardHash}" -->\n` +
      `Claimed by @${actor}. Post a meaningful \`/progress ...\` update within **72 hours** or the claim will be released automatically.` +
      rewardText
    );
    return;
  }

  if (command === '/progress') {
    if (!state.claimant || state.claimant.toLowerCase() !== actor.toLowerCase()) {
      await comment('Only the current claimant can post a bounty progress command.');
      return;
    }
    if (!labelNames().includes('status:claimed')) {
      await comment('Progress can only be recorded while the bounty is in `status:claimed`.');
      return;
    }
    if (payload.length < 15) {
      await comment('Please include a meaningful progress update after `/progress` (at least 15 characters).');
      return;
    }
    await comment(`<!-- telegraph-progress user="${actor}" at="${now}" -->\nProgress recorded for @${actor}: ${payload}`);
    return;
  }

  if (command === '/release') {
    if (!state.claimant) {
      await comment('There is no active claim to release.');
      return;
    }
    const maintainer = await isMaintainer();
    if (state.claimant.toLowerCase() !== actor.toLowerCase() && !maintainer) {
      await comment(`Only @${state.claimant} or a maintainer can release this claim.`);
      return;
    }
    await setStatus('status:open');
    await comment(`<!-- telegraph-release user="${actor}" at="${now}" -->\nClaim released by @${actor}. This bounty is open again.`);
    return;
  }

  if (command === '/submit') {
    const maintainer = await isMaintainer();
    const isClaimant = !!state.claimant && state.claimant.toLowerCase() === actor.toLowerCase();

    if (!maintainer) {
      if (!labelNames().includes('status:claimed') || !isClaimant) {
        if (state.claimant) {
          await comment(`Only the current claimant @${state.claimant} can submit this bounty.`);
        } else {
          await comment('This bounty must be claimed before it can be submitted. Comment `/claim` first.');
        }
        return;
      }
    } else if (!labelNames().includes('status:claimed') && !labelNames().includes('status:open')) {
      await comment('Maintainer `/submit` override is only valid from `status:claimed` or `status:open`.');
      return;
    }

    if (payload.length < 15) {
      await comment('Please include repository/demo/evidence links after `/submit`.');
      return;
    }
    await setStatus('status:review');
    const override = maintainer && !isClaimant ? ' (maintainer override)' : '';
    await comment(`<!-- telegraph-submit user="${actor}" at="${now}" -->\nSubmission from @${actor}${override} moved to **review**.\n\n${payload}`);
    return;
  }

  if (command === '/open') {
    if (!(await isMaintainer())) return;
    await setStatus('status:open');
    await comment(`<!-- telegraph-open user="${actor}" at="${now}" -->\nTriage complete. This bounty is now open for contribution.`);
    return;
  }

  if (command === '/block') {
    if (!(await isMaintainer())) return;
    await setStatus('status:blocked');
    await comment(`<!-- telegraph-block user="${actor}" at="${now}" -->\nMarked blocked by @${actor}.${payload ? `\n\n${payload}` : ''}`);
    return;
  }

  if (command === '/unblock') {
    if (!(await isMaintainer())) return;
    await setStatus(state.claimant ? 'status:claimed' : 'status:open');
    await comment(`<!-- telegraph-unblock user="${actor}" at="${now}" -->\nUnblocked by @${actor}.`);
    return;
  }

  if (command === '/changes') {
    if (!(await isMaintainer())) return;
    if (!labelNames().includes('status:review')) {
      await comment('`/changes` is only valid while the bounty is in `status:review`.');
      return;
    }
    if (!state.claimant) {
      await comment('Cannot request changes because this review has no active claimant to return the bounty to.');
      return;
    }
    if (payload.length < 10) {
      await comment('Please include a clear reason after `/changes` (at least 10 characters).');
      return;
    }
    await setStatus('status:claimed');
    await comment(
      `<!-- telegraph-changes user="${actor}" claimant="${state.claimant}" at="${now}" -->\n` +
      `Changes requested by @${actor}. Returned to @${state.claimant} as **claimed**; the 72-hour progress window restarts now.\n\n${payload}`
    );
    return;
  }

  if (command === '/approve') {
    if (!(await isMaintainer())) return;
    if (!labelNames().includes('status:review')) {
      await comment('`/approve` is only valid while the bounty is in `status:review`.');
      return;
    }
    await setStatus('status:done');
    await github.rest.issues.update({ owner, repo, issue_number, state: 'closed', state_reason: 'completed' });
    await comment(`<!-- telegraph-approve user="${actor}" at="${now}" -->\nVerified and approved by @${actor}. Bounty complete.`);
    return;
  }
};

'use strict';

const {
  parseState,
  snapshotReward,
  quoteMarkdown,
  permissionAllowsMaintenance,
} = require('./bounty_state');
const { STATUS_LABELS, reconcileIssue, recordTransition } = require('./bounty_journal');
const COMMANDS = new Set(['/claim', '/progress', '/release', '/submit', '/open', '/block', '/unblock', '/changes', '/approve']);

module.exports = async function runBountyCommand({ github, context }) {
  const event = context.payload.comment;
  const raw = String(event?.body || '').trim();
  if (raw.length > 8192) return;

  const [command, ...rest] = raw.split(/\s+/);
  if (!COMMANDS.has(command)) return;
  const payload = rest.join(' ').trim();
  const owner = context.repo.owner;
  const repo = context.repo.repo;
  const issue_number = context.issue.number;
  const actor = context.actor;
  if (!Number.isSafeInteger(event.id) || event.id <= 0 || event.user?.type !== 'User' ||
      event.user.login.toLowerCase() !== String(actor).toLowerCase() ||
      !/^[A-Za-z0-9][A-Za-z0-9-]{0,38}$/.test(actor)) return;
  const source = `comment:${event.id}`;

  const issueResp = await github.rest.issues.get({ owner, repo, issue_number });
  let issue = issueResp.data;
  const labelNames = () => issue.labels.map(l => typeof l === 'string' ? l : l.name);

  async function comment(body) {
    await github.rest.issues.createComment({ owner, repo, issue_number,
      body: `<!-- telegraph-reject source="${source}" -->\n${body}` });
  }
  async function comments() {
    return github.paginate(github.rest.issues.listComments, { owner, repo, issue_number, per_page: 100 });
  }
  async function transition(body) {
    await recordTransition({ github, owner, repo, issue_number, source, body });
  }

  const all = await comments();
  const state = parseState(all);
  // Recover a prior accepted command before considering this delivery again.
  if (state.processedSources.has(source)) {
    await reconcileIssue({ github, owner, repo, issue_number, state });
    return;
  }
  if (issue.state !== 'open' || issue.pull_request) return;
  const current = (await github.rest.issues.getComment({ owner, repo, comment_id: event.id })).data;
  if (current.body !== event.body || current.user?.login?.toLowerCase() !== actor.toLowerCase()) return;
  issue = await reconcileIssue({ github, owner, repo, issue_number, state });
  const statuses = labelNames().filter(label => STATUS_LABELS.has(label));
  if (statuses.length !== 1 || statuses[0] === 'status:done') return;
  const now = new Date().toISOString();

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
    if ((reward.text || '').length > 16000) {
      await comment('Reward terms are too long to snapshot safely. A maintainer must shorten the Reward section before claiming.');
      return;
    }
    const rewardHash = reward.sha256 || 'none';
    const rewardText = reward.text
      ? `\n\n**Reward terms locked for this claim** (SHA-256 \`${rewardHash}\`):\n${quoteMarkdown(reward.text)}`
      : '\n\n**Reward terms locked for this claim:** no explicit `## Reward` section was present at claim time.';

    await transition(
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
    await transition(`<!-- telegraph-progress user="${actor}" at="${now}" -->\nProgress recorded for @${actor}: ${payload}`);
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
    await transition(`<!-- telegraph-release user="${actor}" at="${now}" -->\nClaim released by @${actor}. This bounty is open again.`);
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
    const override = maintainer && !isClaimant ? ' (maintainer override)' : '';
    await transition(`<!-- telegraph-submit user="${actor}" at="${now}" -->\nSubmission from @${actor}${override} moved to **review**.\n\n${payload}`);
    return;
  }

  if (command === '/open') {
    if (!(await isMaintainer())) return;
    if (state.claimant || !['status:triage', 'status:open'].includes(statuses[0])) return;
    await transition(`<!-- telegraph-open user="${actor}" at="${now}" -->\nTriage complete. This bounty is now open for contribution.`);
    return;
  }

  if (command === '/block') {
    if (!(await isMaintainer())) return;
    if (!['status:open', 'status:claimed', 'status:review'].includes(statuses[0])) return;
    await transition(`<!-- telegraph-block user="${actor}" at="${now}" -->\nMarked blocked by @${actor}.${payload ? `\n\n${payload}` : ''}`);
    return;
  }

  if (command === '/unblock') {
    if (!(await isMaintainer())) return;
    if (state.status !== 'status:blocked') return;
    await transition(`<!-- telegraph-unblock user="${actor}" at="${now}" -->\nUnblocked by @${actor}.`);
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
    await transition(
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
    if (!state.lastSubmitter) {
      await comment('A recorded submission is required before approval.');
      return;
    }
    if ([state.claimant, state.lastSubmitter].some(user => user?.toLowerCase() === actor.toLowerCase())) {
      await comment('An independent maintainer must review and approve this submission. Claimants and submitters cannot approve their own work.');
      return;
    }
    await transition(`<!-- telegraph-approve user="${actor}" at="${now}" -->\nVerified and approved by @${actor}. Bounty complete. This does not authorize or execute a payout.`);
    return;
  }
};

'use strict';

const { parseState } = require('./bounty_state');

const STATUS_LABELS = new Set([
  'status:triage', 'status:open', 'status:claimed',
  'status:review', 'status:blocked', 'status:done',
]);

// All callers must use the shared Actions concurrency group. This journal is
// recoverable coordination state, not an immutable payment authorization ledger.
async function reconcileIssue({ github, owner, repo, issue_number, state }) {
  let issue = (await github.rest.issues.get({ owner, repo, issue_number })).data;
  if (!state.status) return issue;
  const labels = issue.labels.map(l => typeof l === 'string' ? l : l.name);
  const statuses = labels.filter(l => STATUS_LABELS.has(l));
  if (statuses.length !== 1 || statuses[0] !== state.status) {
    await github.rest.issues.setLabels({
      owner, repo, issue_number,
      labels: [...labels.filter(l => !STATUS_LABELS.has(l)), state.status],
    });
  }
  if (state.status === 'status:done' && issue.state !== 'closed') {
    await github.rest.issues.update({ owner, repo, issue_number, state: 'closed', state_reason: 'completed' });
  }
  issue = (await github.rest.issues.get({ owner, repo, issue_number })).data;
  return issue;
}

async function recordTransition({ github, owner, repo, issue_number, source, body }) {
  if (!/^[a-z0-9:-]+$/.test(source)) throw new Error('Invalid transition source');
  const lines = body.split('\n');
  lines.splice(1, 0, `<!-- telegraph-event source="${source}" -->`);
  // Persist the decision BEFORE its derived labels/closed state. On an ambiguous
  // API failure, rerun the original workflow: read back its source ID first.
  await github.rest.issues.createComment({ owner, repo, issue_number, body: lines.join('\n') });
  const comments = await github.paginate(github.rest.issues.listComments, { owner, repo, issue_number, per_page: 100 });
  const state = parseState(comments);
  await reconcileIssue({ github, owner, repo, issue_number, state });
  return state;
}

module.exports = { STATUS_LABELS, reconcileIssue, recordTransition };

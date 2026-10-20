'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const runCommand = require('../scripts/bounty_commands');
const { parseState, snapshotReward, TRUSTED_BOT_LOGIN } = require('../scripts/bounty_state');

function makeHarness({ labels = ['status:open'], body = '## Reward\nNo monetary/token reward is currently committed.\n', permissions = {} } = {}) {
  const state = {
    issue: { number: 42, labels: [...labels], body, state: 'open' },
    comments: [],
    permissions: { ...permissions },
    nextId: 1,
  };

  function addComment(user, body, created_at = new Date().toISOString()) {
    const c = { id: state.nextId++, user: { login: user, type: user.endsWith('[bot]') ? 'Bot' : 'User' }, body, created_at };
    state.comments.push(c);
    return c;
  }

  const github = {
    rest: {
      issues: {
        get: async () => ({ data: { ...state.issue, labels: state.issue.labels.map(name => ({ name })) } }),
        setLabels: async ({ labels: next }) => { state.issue.labels = [...next]; return { data: {} }; },
        createComment: async ({ body: text }) => ({ data: addComment(TRUSTED_BOT_LOGIN, text) }),
        listComments: async () => ({ data: [...state.comments] }),
        getComment: async ({ comment_id }) => ({ data: state.comments.find(c => c.id === comment_id) }),
        update: async ({ state: nextState, state_reason }) => {
          state.issue.state = nextState;
          state.issue.state_reason = state_reason;
          return { data: state.issue };
        },
      },
      repos: {
        getCollaboratorPermissionLevel: async ({ username }) => ({ data: { permission: state.permissions[username] || 'read' } }),
      },
    },
    paginate: async (fn, args) => {
      const resp = await fn(args);
      return resp.data;
    },
  };

  async function command(actor, text, commentId) {
    const event = commentId ? state.comments.find(c => c.id === commentId) : addComment(actor, text);
    const context = {
      repo: { owner: 'telegraph', repo: 'bounties' },
      issue: { number: 42 },
      actor,
      payload: { comment: event },
    };
    await runCommand({ github, context });
    return event.id;
  }

  return { state, github, command, addComment };
}

async function testForgedMarkersIgnored() {
  const h = makeHarness();
  h.addComment('mallory', '<!-- telegraph-claim user="mallory" at="2099-01-01T00:00:00.000Z" reward_sha256="none" -->');
  await h.command('alice', '/claim');
  assert(h.state.issue.labels.includes('status:claimed'), 'legitimate claim should succeed despite forged user marker');
  const parsed = parseState(h.state.comments);
  assert.strictEqual(parsed.claimant, 'alice');
}

async function testSecondLineMarkerSmugglingIgnored() {
  const comments = [
    {
      id: 1,
      user: { login: TRUSTED_BOT_LOGIN },
      created_at: '2026-10-05T00:00:00.000Z',
      body: '<!-- telegraph-claim user="alice" at="2026-10-05T00:00:00.000Z" reward_sha256="none" -->\nClaimed.',
    },
    {
      id: 2,
      user: { login: TRUSTED_BOT_LOGIN },
      created_at: '2026-10-05T01:00:00.000Z',
      body: '<!-- telegraph-progress user="alice" at="2026-10-05T01:00:00.000Z" -->\nProgress: attacker text\n<!-- telegraph-release user="mallory" at="2026-10-05T01:00:01.000Z" -->',
    },
  ];
  const parsed = parseState(comments);
  assert.strictEqual(parsed.claimant, 'alice');
  assert.strictEqual(parsed.lastProgressAt, '2026-10-05T01:00:00.000Z');
}

async function testUnauthorizedMaintainerCommandRejected() {
  const h = makeHarness({ labels: ['status:review'], permissions: { mallory: 'read' } });
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-claim user="alice" at="2026-10-05T00:00:00.000Z" reward_sha256="none" -->\nClaimed.');
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-submit user="alice" at="2026-10-05T01:00:00.000Z" -->\nSubmitted.');
  await h.command('mallory', '/approve');
  assert(h.state.issue.labels.includes('status:review'));
  assert.strictEqual(h.state.issue.state, 'open');
}

async function testWritePermissionCanApprove() {
  const h = makeHarness({ labels: ['status:review'], permissions: { maintainer: 'write' } });
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-claim user="alice" at="2026-10-05T00:00:00.000Z" reward_sha256="none" -->\nClaimed.');
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-submit user="alice" at="2026-10-05T01:00:00.000Z" -->\nSubmitted.');
  await h.command('maintainer', '/approve');
  assert(h.state.issue.labels.includes('status:done'));
  assert.strictEqual(h.state.issue.state, 'closed');
}

async function testOpenBountySubmitHijackRejected() {
  const h = makeHarness({ labels: ['status:open'], permissions: { mallory: 'read' } });
  await h.command('mallory', '/submit https://example.com/fake-proof');
  assert(h.state.issue.labels.includes('status:open'));
  assert(!h.state.issue.labels.includes('status:review'));
}

async function testClaimantCanSubmit() {
  const h = makeHarness({ labels: ['status:claimed'] });
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-claim user="alice" at="2026-10-05T00:00:00.000Z" reward_sha256="none" -->\nClaimed.');
  await h.command('alice', '/submit https://example.com/repo proof-request-123');
  assert(h.state.issue.labels.includes('status:review'));
}

async function testChangesReturnsToSameClaimant() {
  const h = makeHarness({ labels: ['status:review'], permissions: { maintainer: 'maintain' } });
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-claim user="alice" at="2026-10-05T00:00:00.000Z" reward_sha256="none" -->\nClaimed.');
  h.addComment(TRUSTED_BOT_LOGIN, '<!-- telegraph-submit user="alice" at="2026-10-05T01:00:00.000Z" -->\nSubmitted.');
  await h.command('maintainer', '/changes Please add the missing reproducible benchmark evidence.');
  assert(h.state.issue.labels.includes('status:claimed'));
  const parsed = parseState(h.state.comments);
  assert.strictEqual(parsed.claimant, 'alice');
  assert(parsed.lastProgressAt > '2026-10-05T00:00:00.000Z');
  const last = h.state.comments[h.state.comments.length - 1];
  assert(last.body.includes('Changes requested'));
}

async function testSequentialClaimCollisionRejected() {
  const h = makeHarness();
  await h.command('alice', '/claim');
  await h.command('bob', '/claim');
  const parsed = parseState(h.state.comments);
  assert.strictEqual(parsed.claimant, 'alice');
  assert(h.state.comments.some(c => c.body.includes('not currently open for claiming')));
}

async function testRewardSnapshotAtClaimTime() {
  const initialBody = '## Why this matters\nTest.\n\n## Reward\n- Amount: **500 USD**\n- Payout asset: **USDC**\n- Conversion rule: **1 USD = 1 USDC at payout**\n\n## Claim / submit\n...\n';
  const h = makeHarness({ body: initialBody });
  const expected = snapshotReward(initialBody);
  await h.command('alice', '/claim');
  h.state.issue.body = initialBody.replace('500 USD', '5000 USD');
  const parsed = parseState(h.state.comments);
  assert.strictEqual(parsed.rewardSha256, expected.sha256);
  const claimComment = h.state.comments.find(c => c.body.startsWith('<!-- telegraph-claim'));
  assert(claimComment.body.includes('500 USD'));
  assert(!claimComment.body.includes('5000 USD'));
}

async function testProviderRecruitmentCannotBeClaimed() {
  const h = makeHarness({ labels: ['status:open', 'work:miner', 'opportunity:provider', 'reward:unfunded'] });
  await h.command('alice', '/claim');
  assert(h.state.issue.labels.includes('status:open'));
  assert(!h.state.issue.labels.includes('status:claimed'));
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  assert(h.state.comments.at(-1).body.includes('not a claimable GitHub bounty'));
}

async function testProviderRecruitmentCannotBeApprovedByMaintainer() {
  const h = makeHarness({ labels: ['status:review', 'opportunity:provider'], permissions: { maintainer: 'admin' } });
  await h.command('maintainer', '/approve');
  assert.strictEqual(h.state.issue.state, 'open');
  assert(h.state.issue.labels.includes('status:review'));
  await h.command('maintainer', '/submit https://example.com/proof substantial evidence');
  assert(h.state.issue.labels.includes('status:review'));
}

async function testProviderLeadCanBeOpenedButNotClaimed() {
  const h = makeHarness({ labels: ['status:triage', 'opportunity:provider'], permissions: { maintainer: 'write' } });
  await h.command('maintainer', '/open');
  assert(h.state.issue.labels.includes('status:open'));
  await h.command('bob', '/claim');
  assert(!h.state.issue.labels.includes('status:claimed'));
}

async function testRewardSectionAtEndOfIssueIsLocked() {
  // Issue Forms and hand-written Issues often end with the Reward section.
  const body = '## Why\nTest.\n\n## Reward\n- Amount: **500 USD**\n- Payout asset: **USDC**\n- Conversion rule: **1 USD = 1 USDC at payout**\n- Zone: Zed';
  const snap = snapshotReward(body);
  assert(snap.text, 'a trailing Reward section must be captured');
  assert(snap.text.includes('Zone: Zed'), 'capture must not stop at a stray capital Z');
  assert(snap.text.endsWith('Zone: Zed'));
  const h = makeHarness({ body });
  await h.command('alice', '/claim');
  assert.strictEqual(parseState(h.state.comments).rewardSha256, snap.sha256);
}

async function testRewardSectionAbsentIsNone() {
  const h = makeHarness({ body: '## Why\nNo reward section here.\n' });
  await h.command('alice', '/claim');
  assert.strictEqual(parseState(h.state.comments).rewardSha256, null);
}

async function testOpenRequiresMaintainer() {
  const h = makeHarness({ labels: ['status:triage'], permissions: { maintainer: 'write' } });
  await h.command('mallory', '/open');
  assert(h.state.issue.labels.includes('status:triage'), 'non-maintainer must not open a bounty');
  await h.command('maintainer', '/open');
  assert(h.state.issue.labels.includes('status:open'));
}

async function testProgressRejectedForNonClaimantAndShortText() {
  const h = makeHarness();
  await h.command('alice', '/claim');
  const before = h.state.comments.length;
  await h.command('mallory', '/progress working on it for sure');
  assert(h.state.comments.at(-1).body.includes('Only the current claimant'));
  await h.command('alice', '/progress ok');
  assert(h.state.comments.at(-1).body.includes('at least 15 characters'));
  assert(!h.state.comments.slice(before).some(c => c.body.startsWith('<!-- telegraph-progress')));
  await h.command('alice', '/progress wired the reference fixtures today');
  assert(h.state.comments.at(-1).body.startsWith('<!-- telegraph-progress'));
}

async function testReleaseByClaimantOrMaintainerOnly() {
  const h = makeHarness({ permissions: { maintainer: 'maintain' } });
  await h.command('alice', '/claim');
  await h.command('mallory', '/release');
  assert(h.state.issue.labels.includes('status:claimed'), 'stranger must not release a claim');
  await h.command('maintainer', '/release');
  assert(h.state.issue.labels.includes('status:open'));
  assert.strictEqual(parseState(h.state.comments).claimant, null);
}

async function testApproveOnlyFromReviewAndClosesIssue() {
  const h = makeHarness({ labels: ['status:claimed'], permissions: { maintainer: 'admin' } });
  await h.command('maintainer', '/approve');
  assert.strictEqual(h.state.issue.state, 'open', 'approve must not skip review');
  await h.command('maintainer', '/submit https://example.com/evidence');
  h.state.permissions.reviewer = 'write';
  await h.command('reviewer', '/approve');
  assert.strictEqual(h.state.issue.state, 'closed');
  assert(h.state.issue.labels.includes('status:done'));
}

async function testBlockAndUnblockMaintainerOnly() {
  const h = makeHarness({ permissions: { maintainer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('mallory', '/block stop');
  assert(h.state.issue.labels.includes('status:claimed'));
  await h.command('maintainer', '/block waiting on upstream');
  assert(h.state.issue.labels.includes('status:blocked'));
  await h.command('maintainer', '/unblock');
  assert(h.state.issue.labels.includes('status:claimed'), 'unblock restores claimed when a claim exists');
}

async function testChangesRequiresReasonAndReviewState() {
  const h = makeHarness({ permissions: { maintainer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('alice', '/submit https://example.com/evidence');
  await h.command('maintainer', '/changes no');
  assert(h.state.issue.labels.includes('status:review'), 'short reason must be rejected');
  await h.command('maintainer', '/changes please add the reference fixtures');
  assert(h.state.issue.labels.includes('status:claimed'));
}

function testConcurrencyConfigured() {
  const workflow = fs.readFileSync(path.join(__dirname, '..', '.github', 'workflows', 'bounty-commands.yml'), 'utf8');
  assert(workflow.includes('group: bounty-state-${{ github.repository }}'));
  assert(workflow.includes('cancel-in-progress: false'));
  assert(workflow.includes('queue: max'));
  const stale = fs.readFileSync(path.join(__dirname, '..', '.github', 'workflows', 'stale-claims.yml'), 'utf8');
  assert(stale.includes('group: bounty-state-${{ github.repository }}'));
  assert(stale.includes('queue: max'));
}

async function testCommentFailureDoesNotCreateClaim() {
  const h = makeHarness();
  const createComment = h.github.rest.issues.createComment;
  h.github.rest.issues.createComment = async () => { throw new Error('simulated write failure'); };
  await assert.rejects(h.command('alice', '/claim'), /simulated write failure/);
  assert(h.state.issue.labels.includes('status:open'));
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  h.github.rest.issues.createComment = createComment;
  await h.command('alice', '/claim', h.state.comments[0].id);
  assert.strictEqual(parseState(h.state.comments).claimant, 'alice');
}

async function testRetryRepairsLabelsWithoutDuplicateClaim() {
  const h = makeHarness();
  const setLabels = h.github.rest.issues.setLabels;
  h.github.rest.issues.setLabels = async () => { throw new Error('simulated label failure'); };
  await assert.rejects(h.command('alice', '/claim'), /simulated label failure/);
  assert.strictEqual(parseState(h.state.comments).claimant, 'alice');
  assert(h.state.issue.labels.includes('status:open'));
  h.github.rest.issues.setLabels = setLabels;
  await h.command('alice', '/claim', h.state.comments[0].id);
  assert(h.state.issue.labels.includes('status:claimed'));
  assert.strictEqual(h.state.comments.filter(c => c.body.startsWith('<!-- telegraph-claim')).length, 1);
}

async function testAmbiguousCommentFailureIsNotReplayed() {
  const h = makeHarness();
  const createComment = h.github.rest.issues.createComment;
  h.github.rest.issues.createComment = async args => {
    await createComment(args);
    throw new Error('simulated timeout after write');
  };
  await assert.rejects(h.command('alice', '/claim'), /timeout after write/);
  h.github.rest.issues.createComment = createComment;
  await h.command('alice', '/claim', h.state.comments[0].id);
  assert.strictEqual(h.state.comments.filter(c => c.body.startsWith('<!-- telegraph-claim')).length, 1);
  assert(h.state.issue.labels.includes('status:claimed'));
}

async function testOldDeliveryCannotReclaimReleasedIssue() {
  const h = makeHarness();
  const id = await h.command('alice', '/claim');
  await h.command('alice', '/release');
  await h.command('alice', '/claim', id);
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  assert(h.state.issue.labels.includes('status:open'));
}

async function testSelfApprovalRejected() {
  const h = makeHarness({ permissions: { alice: 'admin', reviewer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('alice', '/submit https://example.com/evidence');
  await h.command('alice', '/approve');
  assert.strictEqual(h.state.issue.state, 'open');
  assert(h.state.comments.at(-1).body.includes('independent maintainer'));
  await h.command('reviewer', '/approve');
  assert.strictEqual(h.state.issue.state, 'closed');
}

async function testApprovalRetryRepairsFailedClose() {
  const h = makeHarness({ permissions: { reviewer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('alice', '/submit https://example.com/evidence');
  const update = h.github.rest.issues.update;
  h.github.rest.issues.update = async () => { throw new Error('simulated close failure'); };
  await assert.rejects(h.command('reviewer', '/approve'), /close failure/);
  h.github.rest.issues.update = update;
  const id = h.state.comments.find(c => c.user.login === 'reviewer').id;
  await h.command('reviewer', '/approve', id);
  assert.strictEqual(h.state.issue.state, 'closed');
  assert.strictEqual(h.state.comments.filter(c => c.body.startsWith('<!-- telegraph-approve')).length, 1);
}

async function testClosedIssueAndBotsCannotClaim() {
  const h = makeHarness();
  h.state.issue.state = 'closed';
  await h.command('alice', '/claim');
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  h.state.issue.state = 'open';
  await h.command('dependabot[bot]', '/claim');
  assert.strictEqual(parseState(h.state.comments).claimant, null);
}

async function testLabelEditsCannotSkipReviewOrReopenCompletedWork() {
  const h = makeHarness({ permissions: { reviewer: 'write' } });
  await h.command('alice', '/claim');
  h.state.issue.labels = ['status:review'];
  await h.command('reviewer', '/approve');
  assert.strictEqual(h.state.issue.state, 'open');
  assert(h.state.issue.labels.includes('status:claimed'));
  await h.command('alice', '/submit https://example.com/evidence');
  await h.command('reviewer', '/approve');
  h.state.issue.state = 'open';
  h.state.issue.labels = ['status:open'];
  await h.command('bob', '/claim');
  assert.strictEqual(h.state.issue.state, 'closed');
  assert(h.state.issue.labels.includes('status:done'));
}

async function testUnsupportedAndOversizedInputDoesNotCallGitHub() {
  const github = new Proxy({}, { get() { throw new Error('unexpected API access'); } });
  for (const body of ['/unknown hello', '/progress ' + 'x'.repeat(8192), 'hello']) {
    await runCommand({ github, context: { payload: { comment: { body } } } });
  }
}

async function testOpenCannotResetAnActiveClaim() {
  const h = makeHarness({ permissions: { reviewer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('reviewer', '/open');
  assert(h.state.issue.labels.includes('status:claimed'));
}

async function testUnblockPreservesReview() {
  const h = makeHarness({ permissions: { reviewer: 'write' } });
  await h.command('alice', '/claim');
  await h.command('alice', '/submit https://example.com/evidence');
  await h.command('reviewer', '/block waiting for independent evidence');
  await h.command('reviewer', '/unblock');
  assert(h.state.issue.labels.includes('status:review'));
}

async function testEditedQueuedCommandIsIgnored() {
  const h = makeHarness();
  const event = h.addComment('alice', '/claim');
  const original = { ...event };
  event.body = '/release';
  await runCommand({ github: h.github, context: { repo: {owner:'telegraph',repo:'bounties'},
    issue: {number:42}, actor:'alice', payload:{comment: original} } });
  assert.strictEqual(parseState(h.state.comments).claimant, null);
}

async function testConflictingLabelsFailClosed() {
  const h = makeHarness({ labels: ['status:open', 'status:review'] });
  await h.command('alice', '/claim');
  assert.strictEqual(parseState(h.state.comments).claimant, null);
}

async function testRejectedClaimCannotBeReplayedAfterRelease() {
  const h = makeHarness();
  await h.command('alice', '/claim');
  const rejected = await h.command('bob', '/claim');
  await h.command('alice', '/release');
  await h.command('bob', '/claim', rejected);
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  assert(h.state.issue.labels.includes('status:open'));
}

async function main() {
  const tests = [
    testForgedMarkersIgnored,
    testSecondLineMarkerSmugglingIgnored,
    testUnauthorizedMaintainerCommandRejected,
    testWritePermissionCanApprove,
    testOpenBountySubmitHijackRejected,
    testClaimantCanSubmit,
    testChangesReturnsToSameClaimant,
    testSequentialClaimCollisionRejected,
    testRewardSnapshotAtClaimTime,
    testProviderRecruitmentCannotBeClaimed,
    testProviderRecruitmentCannotBeApprovedByMaintainer,
    testProviderLeadCanBeOpenedButNotClaimed,
    testRewardSectionAtEndOfIssueIsLocked,
    testRewardSectionAbsentIsNone,
    testOpenRequiresMaintainer,
    testProgressRejectedForNonClaimantAndShortText,
    testReleaseByClaimantOrMaintainerOnly,
    testApproveOnlyFromReviewAndClosesIssue,
    testBlockAndUnblockMaintainerOnly,
    testChangesRequiresReasonAndReviewState,
    testCommentFailureDoesNotCreateClaim,
    testRetryRepairsLabelsWithoutDuplicateClaim,
    testAmbiguousCommentFailureIsNotReplayed,
    testOldDeliveryCannotReclaimReleasedIssue,
    testSelfApprovalRejected,
    testApprovalRetryRepairsFailedClose,
    testClosedIssueAndBotsCannotClaim,
    testLabelEditsCannotSkipReviewOrReopenCompletedWork,
    testUnsupportedAndOversizedInputDoesNotCallGitHub,
    testOpenCannotResetAnActiveClaim,
    testUnblockPreservesReview,
    testEditedQueuedCommandIsIgnored,
    testConflictingLabelsFailClosed,
    testRejectedClaimCannotBeReplayedAfterRelease,
  ];
  for (const test of tests) {
    await test();
    console.log(`PASS ${test.name}`);
  }
  testConcurrencyConfigured();
  console.log('PASS testConcurrencyConfigured');
  console.log(`WORKFLOW TESTS OK: ${tests.length + 1}`);
}

main().catch(err => {
  console.error(err.stack || err);
  process.exit(1);
});

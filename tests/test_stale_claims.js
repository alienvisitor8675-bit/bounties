'use strict';

const assert = require('assert');
const runStaleClaims = require('../scripts/stale_claims');
const { TRUSTED_BOT_LOGIN, parseState } = require('../scripts/bounty_state');

function makeHarness(comments) {
  const state = {
    issue: { number: 42, labels: ['status:claimed'], state: 'open' },
    comments: comments.map((c, i) => ({ id: i + 1, ...c })),
    nextId: comments.length + 1,
  };
  const github = {
    rest: {
      issues: {
        listForRepo: async () => ({ data: [state.issue] }),
        listComments: async () => ({ data: [...state.comments] }),
        get: async () => ({ data: { ...state.issue, labels: state.issue.labels.map(name => ({ name })) } }),
        setLabels: async ({ labels }) => { state.issue.labels = [...labels]; return { data: {} }; },
        createComment: async ({ body }) => {
          state.comments.push({ id: state.nextId++, user: { login: TRUSTED_BOT_LOGIN }, body, created_at: new Date().toISOString() });
          return { data: {} };
        },
      },
    },
    paginate: async (fn, args) => (await fn(args)).data,
  };
  const context = { repo: { owner: 'telegraph', repo: 'bounties' } };
  return { state, github, context };
}

async function testForgedProgressDoesNotKeepStaleClaimAlive() {
  const h = makeHarness([
    {
      user: { login: TRUSTED_BOT_LOGIN },
      created_at: '2020-01-01T00:00:00.000Z',
      body: '<!-- telegraph-claim user="alice" at="2020-01-01T00:00:00.000Z" reward_sha256="none" -->\nClaimed.',
    },
    {
      user: { login: 'mallory' },
      created_at: '2099-01-01T00:00:00.000Z',
      body: '<!-- telegraph-progress user="alice" at="2099-01-01T00:00:00.000Z" -->\nForged progress.',
    },
  ]);
  await runStaleClaims({ github: h.github, context: h.context });
  assert(h.state.issue.labels.includes('status:open'));
  assert(!h.state.issue.labels.includes('status:claimed'));
  assert(h.state.comments.some(c => c.body.includes('automatically released')));
}

async function testTrustedRecentProgressKeepsClaim() {
  const h = makeHarness([
    {
      user: { login: TRUSTED_BOT_LOGIN },
      created_at: '2020-01-01T00:00:00.000Z',
      body: '<!-- telegraph-claim user="alice" at="2020-01-01T00:00:00.000Z" reward_sha256="none" -->\nClaimed.',
    },
    {
      user: { login: TRUSTED_BOT_LOGIN },
      created_at: '2099-01-01T00:00:00.000Z',
      body: '<!-- telegraph-progress user="alice" at="2099-01-01T00:00:00.000Z" -->\nTrusted progress.',
    },
  ]);
  await runStaleClaims({ github: h.github, context: h.context });
  assert(h.state.issue.labels.includes('status:claimed'));
  assert(!h.state.issue.labels.includes('status:open'));
}

async function main() {
  const tests = [testForgedProgressDoesNotKeepStaleClaimAlive, testTrustedRecentProgressKeepsClaim,
    testQueuedProgressPreventsRelease, testReleaseFailurePreservesClaim, testScheduledRecoveryRepairsLabels,
    testFreshProgressOnSecondReadPreventsRelease, testClosedOrReviewIssuesAreNotReleased];
  for (const test of tests) {
    await test();
    console.log(`PASS ${test.name}`);
  }
  console.log(`STALE CLAIM TESTS OK: ${tests.length}`);
}

function staleHarness() {
  return makeHarness([{
    user: { login: TRUSTED_BOT_LOGIN }, created_at: '2020-01-01T00:00:00.000Z',
    body: '<!-- telegraph-claim user="alice" at="2020-01-01T00:00:00.000Z" reward_sha256="none" -->\nClaimed.',
  }]);
}

async function testQueuedProgressPreventsRelease() {
  const h = staleHarness();
  h.state.comments.push({id: h.state.nextId++, user: {login: 'alice', type: 'User'},
    created_at: new Date().toISOString(), body: '/progress Completed the integration and preparing reproducible evidence.'});
  await runStaleClaims(h);
  assert(h.state.issue.labels.includes('status:claimed'));
  assert.strictEqual(parseState(h.state.comments).claimant, 'alice');
}

async function testReleaseFailurePreservesClaim() {
  const h = staleHarness();
  h.github.rest.issues.createComment = async () => { throw new Error('release write failed'); };
  await assert.rejects(runStaleClaims(h), /release write failed/);
  assert(h.state.issue.labels.includes('status:claimed'));
  assert.strictEqual(parseState(h.state.comments).claimant, 'alice');
}

async function testScheduledRecoveryRepairsLabels() {
  const h = staleHarness();
  const setLabels = h.github.rest.issues.setLabels;
  h.github.rest.issues.setLabels = async () => { throw new Error('label write failed'); };
  await assert.rejects(runStaleClaims(h), /label write failed/);
  assert.strictEqual(parseState(h.state.comments).claimant, null);
  h.github.rest.issues.setLabels = setLabels;
  await runStaleClaims(h);
  assert(h.state.issue.labels.includes('status:open'));
  assert.strictEqual(h.state.comments.filter(c => c.body.startsWith('<!-- telegraph-release')).length, 1);
}

async function testFreshProgressOnSecondReadPreventsRelease() {
  const h = staleHarness();
  const listComments = h.github.rest.issues.listComments;
  let reads = 0;
  h.github.rest.issues.listComments = async () => {
    if (++reads === 2) {
      const now = new Date().toISOString();
      h.state.comments.push({id: h.state.nextId++, user: {login: TRUSTED_BOT_LOGIN}, created_at: now,
        body: `<!-- telegraph-progress user="alice" at="${now}" -->\nProgress.`});
    }
    return listComments();
  };
  await runStaleClaims(h);
  assert(h.state.issue.labels.includes('status:claimed'));
}

async function testClosedOrReviewIssuesAreNotReleased() {
  for (const mode of ['closed', 'review']) {
    const h = staleHarness();
    if (mode === 'closed') h.state.issue.state = 'closed';
    else h.state.comments.push({id: h.state.nextId++, user: {login: TRUSTED_BOT_LOGIN},
      created_at: new Date().toISOString(), body: `<!-- telegraph-submit user="alice" at="${new Date().toISOString()}" -->\nSubmitted.`});
    await runStaleClaims(h);
    assert.strictEqual(parseState(h.state.comments).claimant, 'alice');
    assert(!h.state.comments.some(c => c.body.startsWith('<!-- telegraph-release')));
  }
}

main().catch(err => {
  console.error(err.stack || err);
  process.exit(1);
});

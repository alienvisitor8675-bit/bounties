'use strict';

const assert = require('assert');
const runStaleClaims = require('../scripts/stale_claims');
const { TRUSTED_BOT_LOGIN } = require('../scripts/bounty_state');

function makeHarness(comments) {
  const state = {
    issue: { number: 42, labels: ['status:claimed'], state: 'open' },
    comments: comments.map((c, i) => ({ id: i + 1, ...c })),
    nextId: comments.length + 1,
  };
  const github = {
    rest: {
      issues: {
        listForRepo: async () => ({ data: [{ number: 42, labels: [{ name: 'status:claimed' }], state: 'open' }] }),
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
  await testForgedProgressDoesNotKeepStaleClaimAlive();
  console.log('PASS testForgedProgressDoesNotKeepStaleClaimAlive');
  await testTrustedRecentProgressKeepsClaim();
  console.log('PASS testTrustedRecentProgressKeepsClaim');
  console.log('STALE CLAIM TESTS OK: 2');
}

main().catch(err => {
  console.error(err.stack || err);
  process.exit(1);
});

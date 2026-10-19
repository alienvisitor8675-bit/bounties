'use strict';

const crypto = require('crypto');

const TRUSTED_BOT_LOGIN = 'github-actions[bot]';
const ISO_UTC = '\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}Z';
const GH_USER = '[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})(?:\\[bot\\])?';

const patterns = {
  claim: new RegExp(`^<!-- telegraph-claim user="(${GH_USER})" at="(${ISO_UTC})" reward_sha256="([a-f0-9]{64}|none)" -->$`),
  progress: new RegExp(`^<!-- telegraph-progress user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  release: new RegExp(`^<!-- telegraph-release user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  submit: new RegExp(`^<!-- telegraph-submit user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  changes: new RegExp(`^<!-- telegraph-changes user="(${GH_USER})" claimant="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  open: new RegExp(`^<!-- telegraph-open user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  block: new RegExp(`^<!-- telegraph-block user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  unblock: new RegExp(`^<!-- telegraph-unblock user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  approve: new RegExp(`^<!-- telegraph-approve user="(${GH_USER})" at="(${ISO_UTC})" -->$`),
  staleWarning: new RegExp(`^<!-- telegraph-stale-warning claimant="(${GH_USER})" claimed_at="(${ISO_UTC})" -->$`),
};

function loginOf(comment) {
  return String(comment?.user?.login || '').toLowerCase();
}

function firstLine(body) {
  return String(body || '').split(/\r?\n/, 1)[0].trim();
}

function parseTrustedControl(comment) {
  if (loginOf(comment) !== TRUSTED_BOT_LOGIN) return null;
  const line = firstLine(comment?.body);
  let m;

  if ((m = line.match(patterns.claim))) {
    return { type: 'claim', user: m[1], at: m[2], rewardSha256: m[3] };
  }
  if ((m = line.match(patterns.progress))) {
    return { type: 'progress', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.release))) {
    return { type: 'release', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.submit))) {
    return { type: 'submit', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.changes))) {
    return { type: 'changes', user: m[1], claimant: m[2], at: m[3] };
  }
  if ((m = line.match(patterns.open))) {
    return { type: 'open', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.block))) {
    return { type: 'block', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.unblock))) {
    return { type: 'unblock', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.approve))) {
    return { type: 'approve', user: m[1], at: m[2] };
  }
  if ((m = line.match(patterns.staleWarning))) {
    return { type: 'stale-warning', claimant: m[1], claimedAt: m[2] };
  }
  return null;
}

function orderedComments(comments) {
  return [...comments].sort((a, b) => {
    const ta = Date.parse(a?.created_at || '') || 0;
    const tb = Date.parse(b?.created_at || '') || 0;
    if (ta !== tb) return ta - tb;
    return Number(a?.id || 0) - Number(b?.id || 0);
  });
}

function parseState(comments) {
  let claimant = null;
  let claimedAt = null;
  let lastProgressAt = null;
  let lastSubmitter = null;
  let rewardSha256 = null;

  for (const comment of orderedComments(comments)) {
    const ctl = parseTrustedControl(comment);
    if (!ctl) continue;

    if (ctl.type === 'claim') {
      claimant = ctl.user;
      claimedAt = ctl.at;
      lastProgressAt = ctl.at;
      rewardSha256 = ctl.rewardSha256 === 'none' ? null : ctl.rewardSha256;
    } else if (ctl.type === 'progress') {
      if (claimant && ctl.user.toLowerCase() === claimant.toLowerCase()) {
        lastProgressAt = ctl.at;
      }
    } else if (ctl.type === 'changes') {
      if (claimant && ctl.claimant.toLowerCase() === claimant.toLowerCase()) {
        // A changes request starts a fresh work window for the preserved claimant.
        lastProgressAt = ctl.at;
      }
    } else if (ctl.type === 'release') {
      claimant = null;
      claimedAt = null;
      lastProgressAt = null;
      lastSubmitter = null;
      rewardSha256 = null;
    } else if (ctl.type === 'submit') {
      lastSubmitter = ctl.user;
    }
  }

  return { claimant, claimedAt, lastProgressAt, lastSubmitter, rewardSha256 };
}

function isStaleWarningFor(comment, claimant, claimedAt) {
  const ctl = parseTrustedControl(comment);
  return !!ctl && ctl.type === 'stale-warning' &&
    ctl.claimant.toLowerCase() === String(claimant).toLowerCase() &&
    ctl.claimedAt === claimedAt;
}

function extractRewardSection(issueBody) {
  const body = String(issueBody || '').replace(/\r\n/g, '\n');
  const match = body.match(/^## Reward\s*\n([\s\S]*?)(?=^##\s|(?![\s\S]))/m);
  if (!match) return null;
  return match[1].trim().replace(/[ \t]+$/gm, '');
}

function snapshotReward(issueBody) {
  const section = extractRewardSection(issueBody);
  if (!section) return { text: null, sha256: null };
  const text = section.trim();
  return {
    text,
    sha256: crypto.createHash('sha256').update(text, 'utf8').digest('hex'),
  };
}

function quoteMarkdown(text) {
  return String(text || '').split('\n').map(line => `> ${line}`).join('\n');
}

function permissionAllowsMaintenance(permission) {
  return ['write', 'maintain', 'admin'].includes(String(permission || '').toLowerCase());
}

module.exports = {
  TRUSTED_BOT_LOGIN,
  parseTrustedControl,
  parseState,
  isStaleWarningFor,
  extractRewardSection,
  snapshotReward,
  quoteMarkdown,
  permissionAllowsMaintenance,
  _patterns: patterns,
};

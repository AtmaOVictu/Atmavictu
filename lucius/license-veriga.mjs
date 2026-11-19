import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const VERSION_PATTERN = /^(\d+\.\d{4} × 10⁴) ⊙ ENTRY SEAL\b/m;
const MACHINE_RECORD_PATTERN = /## Machine record\b[\s\S]*?```json\s*([\s\S]*?)\s*```/;
const HISTORY_PATTERN = '^[0-9]+\\.[0-9]{4} × 10⁴ ⊙ ENTRY SEAL';
const HISTORY_SCOPE = 'First-parent LICENSE.md history from current HEAD; follow path renames and select commits with a versioned ENTRY SEAL.';
const REPORT_FORMAT = 'vbl-license-chain/v2';

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function decodeUtf8(bytes, label) {
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  } catch {
    throw new Error(`${label}: invalid UTF-8`);
  }
}

function parseLicense(bytes, label) {
  const text = decodeUtf8(bytes, label);
  const header = text.match(VERSION_PATTERN);
  const version = header?.[1];
  if (!version) throw new Error(`${label}: missing versioned ENTRY SEAL`);

  const recordText = text.match(MACHINE_RECORD_PATTERN)?.[1];
  if (!recordText) throw new Error(`${label}: missing JSON Machine record`);

  let record;
  try {
    record = JSON.parse(recordText);
  } catch (error) {
    throw new Error(`${label}: invalid Machine record JSON (${error.message})`);
  }
  if (!record || typeof record !== 'object' || Array.isArray(record)) {
    throw new Error(`${label}: Machine record must be a JSON object`);
  }
  return { version, record };
}

function predecessorVersion(record, label) {
  const predecessor = record.predecessor;
  if (predecessor === null || predecessor === undefined) return null;
  if (!predecessor || typeof predecessor !== 'object' || Array.isArray(predecessor) ||
      typeof predecessor.version !== 'string' || !predecessor.version) {
    throw new Error(`${label}: invalid predecessor record`);
  }
  return predecessor.version;
}

function git(root, args, encoding = 'utf8') {
  return execFileSync('git', args, {
    cwd: root,
    encoding,
    maxBuffer: 8 * 1024 * 1024,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function gitBlobForWorkingFile(root, bytes) {
  return execFileSync('git', ['hash-object', '--path=LICENSE.md', '--stdin'], {
    cwd: root,
    input: bytes,
    encoding: 'utf8',
    maxBuffer: 8 * 1024 * 1024,
    stdio: ['pipe', 'pipe', 'pipe'],
  }).trim();
}

function addCheck(checks, id, status, detail, interpretation, evidence = {}) {
  for (const field of ['observation', 'inference', 'limitation']) {
    if (typeof interpretation?.[field] !== 'string' || !interpretation[field].trim()) {
      throw new TypeError(`${id}: ${field} must be a non-empty string`);
    }
  }
  checks.push({ id, status, detail, ...interpretation, ...evidence });
}

function isWithinRoot(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative !== '' && relative !== '..' &&
    !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function verifyManifest(root, current, checks) {
  const manifestPath = path.join(root, 'LICENSE-MANIFEST-V2.json');
  let manifest;
  try {
    manifest = JSON.parse(decodeUtf8(fs.readFileSync(manifestPath), 'LICENSE-MANIFEST-V2.json'));
  } catch (error) {
    addCheck(checks, 'manifest_read', 'FAIL', error.message, {
      observation: `Reading or parsing LICENSE-MANIFEST-V2.json failed: ${error.message}`,
      inference: 'The manifest could not be inspected as JSON.',
      limitation: 'No conclusion about the manifest entries or their relationship to the license can be drawn.',
    });
    return { version: null, checked: 0, total: 0, declaredTotal: null };
  }

  if (!Array.isArray(manifest.items)) {
    addCheck(checks, 'manifest_items', 'FAIL', 'Manifest items must be an array', {
      observation: 'The parsed manifest does not contain an items array.',
      inference: 'The listed manifest entries cannot be iterated for integrity checks.',
      limitation: 'This structural result does not assess any file bytes or inventory completeness.',
    });
    return { version: manifest.version ?? null, checked: 0, total: 0, declaredTotal: null };
  }

  const declaredTotal = Number.isSafeInteger(manifest.statistics?.total_items) &&
    manifest.statistics.total_items >= 0
    ? manifest.statistics.total_items
    : null;
  addCheck(
    checks,
    'manifest_inventory_count',
    declaredTotal === null
      ? 'UNVERIFIED'
      : declaredTotal === manifest.items.length
        ? 'PASS'
        : 'UNVERIFIED',
    declaredTotal === null
      ? 'Manifest does not provide a valid statistics.total_items value; inventory completeness is not assessed'
      : declaredTotal === manifest.items.length
        ? `statistics.total_items matches the ${manifest.items.length} listed items; completeness is not established by this count`
        : `statistics.total_items says ${declaredTotal}, while items lists ${manifest.items.length}; field meaning and inventory completeness are not established by this count`,
    {
      observation: declaredTotal === null
      ? `A valid statistics.total_items value is absent; items lists ${manifest.items.length} entries.`
      : `statistics.total_items is ${declaredTotal}; items lists ${manifest.items.length} entries.`,
      inference: declaredTotal === manifest.items.length
      ? 'The declared count agrees with the number of listed entries.'
      : 'The count alone cannot establish what the field means or whether the listed inventory is complete.',
      limitation: 'Count agreement does not prove that every relevant file is listed or that the count has a defined scope.',
    },
    { declaredTotal, listedItems: manifest.items.length },
  );

  const manifestVersionMatches = manifest.version === current.version;
  addCheck(
    checks,
    'manifest_version',
    manifestVersionMatches ? 'PASS' : 'FAIL',
    manifestVersionMatches
      ? `Manifest and living door both identify ${current.version}`
      : `Manifest says ${manifest.version ?? '(missing)'}; living door says ${current.version}`,
    {
      observation: `Manifest version is ${manifest.version ?? '(missing)'}; ENTRY SEAL version is ${current.version}.`,
      inference: manifestVersionMatches
      ? 'The two version labels agree.'
      : 'The two version labels disagree.',
      limitation: 'Matching version labels do not establish that the manifest entries match their files; that is checked separately.',
    },
    { manifestVersion: manifest.version ?? null, licenseVersion: current.version },
  );

  const seen = new Set();
  const failures = [];
  let checked = 0;
  let licenseEntries = 0;

  for (const item of manifest.items) {
    if (!item || typeof item.path !== 'string' || !item.path) {
      failures.push('manifest item has no path');
      continue;
    }
    if (seen.has(item.path)) {
      failures.push(`${item.path}: duplicate manifest entry`);
      continue;
    }
    seen.add(item.path);
    if (item.path === 'LICENSE.md') licenseEntries += 1;

    const segments = item.path.split(/[\\/]/);
    if (path.isAbsolute(item.path) || path.win32.isAbsolute(item.path) || segments.includes('..')) {
      failures.push(`${item.path}: path escapes the repository`);
      continue;
    }

    const filePath = path.resolve(root, ...segments);
    if (!isWithinRoot(root, filePath)) {
      failures.push(`${item.path}: path escapes the repository`);
      continue;
    }

    if (!Number.isSafeInteger(item.size_bytes) || item.size_bytes < 0 ||
        typeof item.sha256 !== 'string' || !/^[0-9a-f]{64}$/i.test(item.sha256)) {
      failures.push(`${item.path}: invalid size_bytes or SHA-256`);
      continue;
    }

    let bytes;
    try {
      const realPath = fs.realpathSync(filePath);
      if (!isWithinRoot(root, realPath)) {
        failures.push(`${item.path}: resolved path escapes the repository`);
        continue;
      }
      bytes = fs.readFileSync(realPath);
    } catch {
      failures.push(`${item.path}: file is missing or unreadable`);
      continue;
    }

    checked += 1;
    const actualHash = sha256(bytes);
    if (bytes.length !== item.size_bytes || actualHash.toLowerCase() !== item.sha256.toLowerCase()) {
      failures.push(
        `${item.path}: expected ${item.size_bytes} bytes / ${item.sha256.toLowerCase()}, ` +
        `found ${bytes.length} bytes / ${actualHash}`,
      );
    }
  }

  if (licenseEntries !== 1) {
    failures.push(`expected exactly one LICENSE.md entry, found ${licenseEntries}`);
  }
  const manifestMatches = failures.length === 0;
  addCheck(
    checks,
    'manifest_integrity',
    manifestMatches ? 'PASS' : 'FAIL',
    manifestMatches
      ? `${checked}/${manifest.items.length} manifest bodies match their size and SHA-256`
      : failures.join('; '),
    {
      observation: manifestMatches
        ? `All ${checked} readable entries in the listed ${manifest.items.length} paths matched their declared size and SHA-256.`
        : `Checked ${checked} listed entries; discrepancies or invalid entries: ${failures.join('; ')}.`,
      inference: manifestMatches
        ? 'The checked listed files match their manifest byte counts and hashes.'
        : 'At least one listed entry is invalid, unavailable, outside the repository, duplicated, or differs from its declared bytes.',
      limitation: 'This check covers only paths listed in the manifest; it does not establish that the inventory is complete or that the manifest is authoritative.',
    },
    { checked, total: manifest.items.length },
  );

  return {
    version: manifest.version ?? null,
    checked,
    total: manifest.items.length,
    declaredTotal,
  };
}

function verifyV1Manifest(root, current, currentBytes, checks) {
  const manifestPath = path.join(root, 'LICENSE-MANIFEST');
  let manifest;
  try {
    manifest = JSON.parse(decodeUtf8(fs.readFileSync(manifestPath), 'LICENSE-MANIFEST'));
  } catch (error) {
    // V1 manifest je neobvezni krizni sklic. Če manjka (ENOENT), se preskoči brez checka;
    // če obstaja, ampak je poškodovan, je to FAIL.
    if (error.code === 'ENOENT') {
      return { version: null, matched: false };
    }
    addCheck(checks, 'v1_manifest_read', 'FAIL', error.message, {
      observation: `Reading or parsing LICENSE-MANIFEST (v1) failed: ${error.message}`,
      inference: 'The v1 manifest could not be inspected as JSON.',
      limitation: 'No conclusion about the v1 manifest entries or their relationship to the license can be drawn.',
    });
    return { version: null, matched: false };
  }

  if (!Array.isArray(manifest.items)) {
    addCheck(checks, 'v1_manifest_items', 'FAIL', 'V1 manifest items must be an array', {
      observation: 'The parsed v1 manifest does not contain an items array.',
      inference: 'The listed v1 manifest entries cannot be iterated for integrity checks.',
      limitation: 'This structural result does not assess any file bytes.',
    });
    return { version: manifest.version ?? null, matched: false };
  }

  const licenseItem = manifest.items.find((item) => item && item.path === 'LICENSE.md');
  if (!licenseItem) {
    addCheck(checks, 'v1_manifest_license_slot', 'FAIL', 'No LICENSE.md item in v1 manifest', {
      observation: 'The v1 manifest lists no item with path LICENSE.md.',
      inference: 'The v1 manifest does not identify the living door.',
      limitation: 'This is a structural result about the v1 manifest, not about the license bytes.',
    });
    return { version: manifest.version ?? null, matched: false };
  }

  // Normalize the working file to LF — the byte stream the chain publishes (§0a, PADC-66).
  const text = decodeUtf8(currentBytes, 'LICENSE.md');
  const lfBytes = Buffer.from(text.replace(/\r\n/g, '\n'), 'utf8');
  const actualHash = sha256(lfBytes).toLowerCase();
  const declaredHash = String(licenseItem.sha256 ?? '').toLowerCase();
  const sizeMatch = lfBytes.length === Number(licenseItem.size_bytes);
  const hashMatch = actualHash === declaredHash && declaredHash.length === 64;
  const matched = sizeMatch && hashMatch;

  addCheck(checks, 'v1_manifest_license_slot', matched ? 'PASS' : 'FAIL', matched
    ? `V1 manifest LICENSE.md slot matches the byte stream the chain publishes (${lfBytes.length} B / ${actualHash})`
    : `V1 manifest LICENSE.md slot declares ${licenseItem.size_bytes} B / ${licenseItem.sha256}; byte stream publishes ${lfBytes.length} B / ${actualHash}`,
  {
    observation: `V1 manifest LICENSE.md slot: ${licenseItem.size_bytes} B / ${licenseItem.sha256}; normalized LF byte stream: ${lfBytes.length} B / ${actualHash}.`,
    inference: matched
      ? 'The tracked v1 manifest agrees with the byte stream the chain publishes.'
      : 'The tracked v1 manifest disagrees with the byte stream the chain publishes (manifest drift).',
    limitation: 'This check covers only the LICENSE.md slot of the v1 manifest; other item slots are not checked here.',
  },
  { matched, sizeBytes: lfBytes.length, sha256: actualHash });

  return { version: manifest.version ?? null, matched };
}

function verifyGitHistory(root, current, currentBytes, checks) {
  let commits;
  try {
    commits = git(root, [
      'log', '--first-parent', '--follow', '-G', HISTORY_PATTERN, '--format=%H', '--', 'LICENSE.md',
    ]).trim().split(/\r?\n/).filter(Boolean);
  } catch (error) {
    addCheck(checks, 'git_history', 'FAIL', `Could not read LICENSE.md history: ${error.message}`, {
      observation: `The scoped Git history query failed: ${error.message}`,
      inference: 'The requested receipt scan did not complete.',
      limitation: 'No conclusion about receipts inside or outside the requested history scope can be drawn.',
    });
    return { receipts: [], source: null };
  }

  let headCommit;
  let headLicenseBlob;
  try {
    headCommit = git(root, ['rev-parse', 'HEAD']).trim();
    headLicenseBlob = git(root, ['rev-parse', 'HEAD:LICENSE.md']).trim();
    addCheck(checks, 'git_head', 'PASS', `Repository HEAD is ${headCommit}`, {
      observation: `Git resolved HEAD to commit ${headCommit} and LICENSE.md to blob ${headLicenseBlob}.`,
      inference: 'The current repository head and its tracked LICENSE.md blob are addressable.',
      limitation: 'Resolvable Git object IDs do not establish who authored or authorized the content.',
    }, { headCommit, headLicenseBlob });
  } catch (error) {
    addCheck(checks, 'git_head', 'FAIL', `Could not identify repository HEAD: ${error.message}`, {
      observation: `Resolving HEAD or HEAD:LICENSE.md failed: ${error.message}`,
      inference: 'A complete link between the working license and the current Git head cannot be checked.',
      limitation: 'This does not identify a cause beyond the reported Git resolution failure.',
    });
  }

  const receipts = [];
  const errors = [];
  for (const commit of [...commits].reverse()) {
    try {
      const bytes = git(root, ['show', `${commit}:LICENSE.md`], null);
      const parsed = parseLicense(bytes, `${commit}:LICENSE.md`);
      if (parsed.record.version !== parsed.version) {
        throw new Error(`ENTRY SEAL says ${parsed.version}; Machine record says ${parsed.record.version ?? '(missing)'}`);
      }
      const blob = git(root, ['rev-parse', `${commit}:LICENSE.md`]).trim();
      const previousVersion = predecessorVersion(parsed.record, `${commit}:LICENSE.md`);
      receipts.push({
        version: parsed.version,
        predecessorVersion: previousVersion,
        commit,
        committedAt: git(root, ['show', '-s', '--format=%cI', commit]).trim(),
        blob,
        sha256: sha256(bytes),
        sizeBytes: bytes.length,
      });
    } catch (error) {
      errors.push(`${commit}: ${error.message}`);
    }
  }

  if (errors.length > 0) {
    addCheck(checks, 'git_history', 'FAIL', errors.join('; '), {
      observation: `${receipts.length} receipts were parsed; ${errors.length} selected commit(s) could not be parsed: ${errors.join('; ')}.`,
      inference: 'The selected history contains at least one receipt that could not be validated.',
      limitation: `The scan is limited to ${HISTORY_SCOPE}`,
    }, { receipts: receipts.length });
    return { receipts, source: headCommit ? { headCommit, headLicenseBlob } : null };
  }
  const receiptsFound = receipts.length > 0;
  addCheck(
    checks,
    'git_history',
    receiptsFound ? 'PASS' : 'UNVERIFIED',
    receiptsFound
      ? `Read ${receipts.length} version-bearing LICENSE.md commits in the first-parent history from HEAD`
      : 'No version-bearing LICENSE.md commits found',
    {
      observation: `The scoped scan found ${receipts.length} version-bearing LICENSE.md commit(s).`,
      inference: receiptsFound
        ? 'The reported receipts were parsed from matching commits in the scanned history.'
        : 'No receipt was established by this scan.',
      limitation: `The scan covers only ${HISTORY_SCOPE} It does not establish that no other receipts exist elsewhere.`,
    },
    { receipts: receipts.length },
  );

  const linkFailures = [];
  for (let index = 0; index < receipts.length; index += 1) {
    const receipt = receipts[index];
    const previous = receipts[index - 1];
    if (!previous) continue;
    if (receipt.predecessorVersion !== previous.version) {
      linkFailures.push(
        `${receipt.version} records predecessor ${receipt.predecessorVersion ?? '(missing)'}, ` +
        `but the preceding published receipt is ${previous.version}`,
      );
    }
  }
  const linksStatus = linkFailures.length
    ? 'FAIL'
    : receipts.length >= 2 || receipts[0]?.predecessorVersion === null
      ? 'PASS'
      : 'UNVERIFIED';
  const linksDetail = linkFailures.length
    ? linkFailures.join('; ')
    : linksStatus === 'PASS'
      ? 'Every recorded predecessor matches the preceding Git receipt, or the sole receipt declares itself a root'
      : 'No predecessor link could be assessed from the available receipts';
  const linksObservation = receipts.length >= 2
    ? linkFailures.length
      ? linkFailures.join('; ')
      : `${receipts.length - 1} predecessor link(s) compared; every compared link matched.`
    : receipts.length === 1 && receipts[0].predecessorVersion === null
      ? 'One receipt was found and it explicitly has no predecessor; there are no links to compare.'
      : `Found ${receipts.length} receipt(s); no predecessor link could be compared.`;
  addCheck(
    checks,
    'predecessor_links',
    linksStatus,
    linksDetail,
    {
      observation: linksObservation,
      inference: linksStatus === 'FAIL'
        ? 'At least one recorded predecessor differs from the preceding receipt in the scanned history.'
        : linksStatus === 'PASS'
          ? 'All predecessor links available in this scan are consistent, or the sole receipt declares itself a root.'
          : 'The available receipts do not provide enough adjacent entries to assess a predecessor link.',
      limitation: `Only adjacent receipts in ${HISTORY_SCOPE} are compared; this does not verify ancestors outside that scope.`,
    },
    { linksChecked: Math.max(0, receipts.length - 1) },
  );

  const first = receipts[0];
  const anchorStatus = !first
    ? 'UNVERIFIED'
    : first.predecessorVersion
      ? 'UNVERIFIED'
      : 'PASS';
  addCheck(
    checks,
    'history_anchor',
    anchorStatus,
    !first
      ? 'No version-bearing receipt was found, so no history anchor can be identified'
      : first.predecessorVersion
      ? `The first receipt found by the first-parent scan from HEAD is ${first.version}; its predecessor ${first.predecessorVersion} has no receipt in that scanned history`
      : 'The first receipt found by the first-parent scan from HEAD is explicitly a root with no predecessor',
    {
      observation: !first
        ? 'The scoped scan returned no version-bearing receipts.'
        : `The first receipt in the scan is ${first.version}; its recorded predecessor is ${first.predecessorVersion ?? '(none)'}.`,
      inference: anchorStatus === 'PASS'
        ? 'The first receipt in the scanned scope explicitly declares no predecessor.'
        : first
          ? 'A predecessor is named but no matching receipt was found earlier in the scanned scope.'
          : 'The scan provides no first receipt from which to assess an anchor.',
      limitation: `The anchor is limited to ${HISTORY_SCOPE}; an earlier receipt may exist outside that scope.`,
    },
    { firstVersion: first?.version ?? null, predecessorVersion: first?.predecessorVersion ?? null },
  );

  const latest = receipts.at(-1);
  const workingBlob = gitBlobForWorkingFile(root, currentBytes);
  const headBlob = git(root, ['rev-parse', 'HEAD:LICENSE.md']).trim();
  const sameAsHead = workingBlob === headBlob;
  const sameAsLatestReceipt = latest?.version === current.version && latest.blob === workingBlob;
  const currentMatchesReceipt = sameAsHead && sameAsLatestReceipt;
  addCheck(
    checks,
    'current_receipt',
    currentMatchesReceipt ? 'PASS' : 'FAIL',
    currentMatchesReceipt
      ? `Working LICENSE.md matches HEAD and latest receipt ${latest.version}`
      : `Working LICENSE.md ${sameAsHead ? 'matches' : 'does not match'} HEAD and ` +
        `${sameAsLatestReceipt ? 'matches' : 'does not match'} the latest scanned receipt ${latest?.version ?? '(none)'}`,
    {
      observation: `Working Git blob is ${workingBlob}; HEAD blob is ${headBlob} (match: ${sameAsHead}); ` +
        `latest scanned receipt is ${latest?.version ?? '(none)'} (match: ${sameAsLatestReceipt}).`,
      inference: currentMatchesReceipt
        ? 'The working license matches both the tracked HEAD blob and the latest receipt in the scanned history.'
        : sameAsHead
          ? 'The working license matches the tracked HEAD blob but does not match the latest scanned receipt.'
          : 'The working license does not match the tracked HEAD blob.',
      limitation: 'A byte-level match establishes identity within this comparison, not authorship, authorization, or legal validity.',
    },
    {
      workingTreeSha256: sha256(currentBytes),
      workingGitBlob: workingBlob,
      headGitBlob: headBlob,
      latestReceipt: latest?.version ?? null,
    },
  );

  return { receipts, source: headCommit ? { headCommit, headLicenseBlob } : null };
}

export function verifyLicenseChain(root = ROOT) {
  const resolvedRoot = fs.realpathSync(path.resolve(root));
  const checks = [];
  let current;
  let currentBytes;

  try {
    currentBytes = fs.readFileSync(path.join(resolvedRoot, 'LICENSE.md'));
    current = parseLicense(currentBytes, 'LICENSE.md');
  } catch (error) {
    addCheck(checks, 'living_door', 'FAIL', error.message, {
      observation: `Reading or parsing LICENSE.md failed: ${error.message}`,
      inference: 'The current file could not be established as a versioned license record.',
      limitation: 'This is a read/format result, not an assessment of authorship or legal validity.',
    });
    return {
      format: REPORT_FORMAT,
      status: 'FAIL',
      current: null,
      manifest: { version: null, checked: 0, total: 0, declaredTotal: null },
      source: null,
      historyScope: HISTORY_SCOPE,
      receipts: [],
      checks,
    };
  }

  const recordVersionMatches = current.record.version === current.version;
  addCheck(
    checks,
    'living_door',
    recordVersionMatches ? 'PASS' : 'FAIL',
    recordVersionMatches
      ? `ENTRY SEAL and Machine record identify ${current.version}`
      : `ENTRY SEAL says ${current.version}; Machine record says ${current.record.version ?? '(missing)'}`,
    {
      observation: `ENTRY SEAL version is ${current.version}; Machine record version is ${current.record.version ?? '(missing)'}.`,
      inference: recordVersionMatches
        ? 'The two version fields inside the current license agree.'
        : 'The version fields inside the current license disagree.',
      limitation: 'Internal agreement does not establish authorship, authorization, or legal validity.',
    },
    { version: current.version, sha256: sha256(currentBytes), sizeBytes: currentBytes.length },
  );

  const manifest = verifyManifest(resolvedRoot, current, checks);
  const v1Manifest = verifyV1Manifest(resolvedRoot, current, currentBytes, checks);
  const { receipts, source } = verifyGitHistory(resolvedRoot, current, currentBytes, checks);
  const status = checks.some((check) => check.status === 'FAIL')
    ? 'FAIL'
    : checks.some((check) => check.status === 'UNVERIFIED')
      ? 'UNVERIFIED'
      : 'PASS';

  return {
    format: REPORT_FORMAT,
    status,
    current: { version: current.version, sha256: sha256(currentBytes), sizeBytes: currentBytes.length },
    manifest,
    v1Manifest,
    source,
    historyScope: HISTORY_SCOPE,
    receipts,
    checks,
  };
}

function usage() {
  return 'Uporaba: node lucius/license-veriga.mjs [--json] [--root <repo-pot>]';
}

export function main(args = process.argv.slice(2)) {
  let root = ROOT;
  let json = false;
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] === '--json') {
      json = true;
    } else if (args[index] === '--root' && args[index + 1]) {
      root = path.resolve(args[++index]);
    } else if (args[index] === '--help') {
      console.log(usage());
      return 0;
    } else {
      console.error(usage());
      return 2;
    }
  }

  const report = verifyLicenseChain(root);
  if (json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`VBL LICENSE VERIGA: ${report.status}`);
    for (const check of report.checks) {
      console.log(`${check.status.padEnd(10)} ${check.id}: ${check.detail}`);
    }
    console.log(`Receipts: ${report.receipts.length}`);
  }
  return report.status === 'PASS' ? 0 : 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    process.exitCode = main();
  } catch (error) {
    console.error(`LICENSE VERIGA: ${error.message}`);
    process.exitCode = 1;
  }
}

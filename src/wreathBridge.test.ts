import assert from 'node:assert/strict';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
import type { WreathSlot } from './wreathBridge.js';
import { verifyWreath, loadWreathManifest, verifyWreathSlot, readCompanion, readLivingDoor } from './wreathBridge.js';

const ROOT = dirname(fileURLToPath(import.meta.url)) + '/../..';

test('loadWreathManifest lists the LICENSE-*.md witness slots from LICENSE-MANIFEST', () => {
  const slots = loadWreathManifest(ROOT);
  assert.ok(Array.isArray(slots));
  const ar = slots.find((s: WreathSlot) => s.path === 'LICENSE-AR.md');
  assert.ok(ar, 'LICENSE-AR.md wreath slot should be listed');
  assert.ok(typeof ar.sha256 === 'string' && ar.sha256.length === 64);
});

test('verifyWreath reports matched wreath slots against real files', () => {
  const report = verifyWreath(ROOT);
  assert.ok(report.total > 0, 'at least one wreath slot should exist');
  assert.ok(report.matched >= 0);
  assert.ok(['PASS', 'FAIL', 'UNVERIFIED'].includes(report.status));
  for (const result of report.results) {
    assert.ok(typeof result.matched === 'boolean');
    assert.ok(typeof result.actualSize === 'number');
    assert.ok(typeof result.actualSha256 === 'string');
  }
});

test('verifyWreathSlot matches a wreath slot against the chain byte stream', () => {
  const slots = loadWreathManifest(ROOT);
  const ar = slots.find((s) => s.path === 'LICENSE-AR.md');
  assert.ok(ar);
  const result = verifyWreathSlot(ROOT, ar);
  assert.equal(result.path, 'LICENSE-AR.md');
  assert.equal(result.matched, true);
});

test('readCompanion returns LICENSE-SPREHOD.md content or null', () => {
  const sprehod = readCompanion(ROOT, 'LICENSE-SPREHOD.md');
  assert.ok(typeof sprehod === 'string' && sprehod.length > 0);
  assert.ok(sprehod.includes('VERIFICATION BEFORE ASSERTION') || sprehod.includes('the door in one breath'));
  const missing = readCompanion(ROOT, 'does-not-exist.md');
  assert.equal(missing, null);
});

test('readLivingDoor returns LICENSE.md content', () => {
  const door = readLivingDoor(ROOT);
  assert.ok(typeof door === 'string' && door.length > 0);
  assert.ok(door.includes('ENTRY SEAL'));
});

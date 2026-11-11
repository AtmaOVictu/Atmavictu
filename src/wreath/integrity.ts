import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export interface WreathSlot {
  path: string;
  size_bytes: number;
  sha256: string;
  status: string;
  language?: string;
  note?: string;
}

export interface WreathSlotResult extends WreathSlot {
  matched: boolean;
  actualSize: number;
  actualSha256: string;
}

export interface WreathVerification {
  manifestSlots: WreathSlot[];
  results: WreathSlotResult[];
  matched: number;
  total: number;
  status: 'PASS' | 'FAIL' | 'UNVERIFIED';
}

function sha256Hex(bytes: Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex');
}

function readTextFile(filePath: string): string {
  return fs.readFileSync(filePath, 'utf8');
}

/**
 * Normalize the working checkout to LF — the byte stream the chain publishes
 * (§0a, PADC-66: manifest hashes the bytes the chain publishes, never the
 * local CRLF checkout).
 */
function normalizeLf(text: string): Buffer {
  return Buffer.from(text.replace(/\r\n/g, '\n'), 'utf8');
}

export function loadWreathManifest(root: string): WreathSlot[] {
  const manifestPath = path.join(root, 'LICENSE-MANIFEST');
  let manifest: unknown;
  try {
    manifest = JSON.parse(readTextFile(manifestPath));
  } catch {
    return [];
  }
  if (!manifest || typeof manifest !== 'object' || !Array.isArray((manifest as Record<string, unknown>).items)) {
    return [];
  }
  const items = (manifest as Record<string, unknown>).items as unknown[];
  return items
    .filter((item: unknown): item is WreathSlot => {
      if (typeof item !== 'object' || item === null) return false;
      const rec = item as Record<string, unknown>;
      return (
        typeof rec.path === 'string' &&
        rec.path.startsWith('LICENSE-') &&
        rec.path.endsWith('.md') &&
        rec.path !== 'LICENSE.md' &&
        typeof rec.size_bytes === 'number' &&
        typeof rec.sha256 === 'string'
      );
    })
    .map((item: WreathSlot) => {
      const result: WreathSlot = {
        path: item.path,
        size_bytes: item.size_bytes,
        sha256: item.sha256.toLowerCase(),
        status: item.status,
      };
      if (item.language !== undefined) result.language = item.language;
      if (item.note !== undefined) result.note = item.note;
      return result;
    });
}

export function verifyWreathSlot(root: string, slot: WreathSlot): WreathSlotResult {
  const filePath = path.resolve(root, slot.path);
  let actual: Buffer;
  try {
    actual = normalizeLf(readTextFile(filePath));
  } catch {
    return { ...slot, matched: false, actualSize: 0, actualSha256: '' };
  }
  const actualSha256 = sha256Hex(actual).toLowerCase();
  const sizeMatch = actual.length === slot.size_bytes;
  const hashMatch = actualSha256 === slot.sha256 && slot.sha256.length === 64;
  return {
    ...slot,
    matched: sizeMatch && hashMatch,
    actualSize: actual.length,
    actualSha256,
  };
}

export function verifyWreath(root: string): WreathVerification {
  const manifestSlots = loadWreathManifest(root);
  const results = manifestSlots.map((slot) => verifyWreathSlot(root, slot));
  const matched = results.filter((r) => r.matched).length;
  const total = results.length;
  const status = total === 0 ? 'UNVERIFIED' : matched === total ? 'PASS' : 'FAIL';
  return { manifestSlots, results, matched, total, status };
}

/**
 * Read a companion witness file (never the door): LICENSE-SPREHOD.md,
 * LICENSE-SLO.md, LICENSE-LINEAGE.md, etc. Returns null when absent.
 */
export function readCompanion(root: string, name: string): string | null {
  const filePath = path.join(root, name);
  try {
    return readTextFile(filePath);
  } catch {
    return null;
  }
}

export function readLivingDoor(root: string): string | null {
  return readCompanion(root, 'LICENSE.md');
}

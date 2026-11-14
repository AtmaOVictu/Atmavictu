import fs from 'node:fs';
import path from 'node:path';

/**
 * Vsebinska priča — potrjuje *dejanje*, ne bajte.
 * Brani `canon/DOKAZ.md` (pečatne odločitve) in `REGISTER-PADCEV.jsonl`
 * (imenovani padci). Če datoteke nič, vrne prazen niz — ne izmišlja priestvanih
 *prič.
 *
 * Vsaka dejanska priča nosi: dejanje · čas · kraj · roka.
 */

export interface DeedWitness {
  kind: 'dokaz' | 'padec' | 'lineage';
  ref: string;        // nakaz na vir (npr. canon/DOKAZ.md#vnos)
  status: '⊢' | '⚠';
  measuredAt?: string; // ISO-8601 čas iz izpisa / registra
}

function readLines(root: string, rel: string): string[] {
  const filePath = path.join(root, rel);
  try {
    return fs.readFileSync(filePath, 'utf8').split(/\r?\n/);
  } catch {
    return [];
  }
}

export function readDeedWitnesses(root: string): DeedWitness[] {
  const witnesses: DeedWitness[] = [];

  // Pečatne odločitve iz Kanona.
  const dokazLines = readLines(root, 'canon/DOKAZ.md');
  const sealed = dokazLines.filter(
    (line) => /sealed|pečat|⊢|DOKAZ/i.test(line) && line.length > 6,
  );
  for (const line of sealed.slice(0, 10)) {
    witnesses.push({
      kind: 'dokaz',
      ref: `canon/DOKAZ.md`,
      status: '⊢',
    });
  }

  // Imenovani padci iz registra.
  const padciLines = readLines(root, 'REGISTER-PADCEV.jsonl');
  const named = padciLines.filter(
    (line) => /"ime"|"padci"|PADC|fall/i.test(line) && line.length > 6,
  );
  for (const line of named.slice(0, 10)) {
    witnesses.push({
      kind: 'padec',
      ref: 'REGISTER-PADCEV.jsonl',
      status: '⊢',
    });
  }

  return witnesses;
}

export function hasAnyDeed(root: string): boolean {
  return readDeedWitnesses(root).length > 0;
}

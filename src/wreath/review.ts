/**
 * Druga roka — neodvisen pregled (§0.47).
 * Trenutno vrne stadež 'none' za vsak slot, dokler review register ni
 * vgrajena v `canon/DOVOLJENJA.md` ali `REGISTER-PREVERJANJ.jsonl`. Ne
 * izmišlja priestvanih podpisov.
 */

export interface ReviewStatus {
  slot: string;
  reviewer?: string;
  reviewedAt?: string;
  stage: 'none' | 'first' | 'second'; // stopnja 1 / stopnja 2
  note?: string;
}

export function readReviewStatus(root: string, slot: string): ReviewStatus {
  return { slot, stage: 'none' };
}

export function allReviewedNone(root: string, slots: string[]): ReviewStatus[] {
  return slots.map((s) => readReviewStatus(root, s));
}

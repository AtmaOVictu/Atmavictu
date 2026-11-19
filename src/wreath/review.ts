import fs from "node:fs";
import path from "node:path";

/**
 * Druga roka — neodvisen pregled (§0.47).
 * Prebere `REGISTER-PREVERJANJ.jsonl` in za vsak slot izračuna stadež:
 * - 'second' — PASS z neodvisnim pregledovalcem (reviewer ni izvajalka)
 * - 'first' — PASS z izvajalkom (samo prva roka)
 * - 'none' — ni zajemanja v registru za ta slot
 * Ne izmišlja priestvanih podpisov.
 */

export interface ReviewStatus {
  slot: string;
  reviewer?: string;
  reviewedAt?: string;
  stage: 'none' | 'first' | 'second'; // stopnja 1 / stopnja 2
  note?: string;
}

function readRegisterEntries(root: string): Array<Record<string, unknown>> {
  try {
    const raw = fs.readFileSync(path.join(root, "REGISTER-PREVERJANJ.jsonl"), "utf8");
    const entries: Array<Record<string, unknown>> = [];
    for (const line of raw.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      entries.push(JSON.parse(trimmed) as Record<string, unknown>);
    }
    return entries;
  } catch {
    return [];
  }
}

function isIndependent(reviewer: unknown): boolean {
  if (typeof reviewer !== "string") return false;
  const lowered = reviewer.toLowerCase();
  return !lowered.includes("izvajalka") && !lowered.includes("executor");
}

export function readReviewStatus(root: string, slot: string): ReviewStatus {
  for (const entry of readRegisterEntries(root)) {
    const subject = entry.subject;
    if (typeof subject === "string" && subject.includes(slot)) {
      const result = entry.result;
      const reviewer =
        typeof entry.reviewer === "string" ? entry.reviewer : undefined;
      const reviewedAt =
        typeof entry.timestamp === "string" ? entry.timestamp : undefined;
      const note =
        typeof entry.limitations === "string" ? entry.limitations : undefined;
      if (result === "PASS") {
        return {
          slot,
          ...(reviewer !== undefined ? { reviewer } : {}),
          ...(reviewedAt !== undefined ? { reviewedAt } : {}),
          stage: isIndependent(entry.reviewer) ? "second" : "first",
          ...(note !== undefined ? { note } : {}),
        };
      }
      return {
        slot,
        ...(reviewer !== undefined ? { reviewer } : {}),
        ...(reviewedAt !== undefined ? { reviewedAt } : {}),
        stage: "none",
        ...(note !== undefined ? { note } : {}),
      };
    }
  }
  return { slot, stage: "none" };
}

export function allReviewedNone(root: string, slots: string[]): ReviewStatus[] {
  return slots.map((s) => readReviewStatus(root, s));
}

import assert from "node:assert/strict";
import { test } from "node:test";
import { readReviewStatus, allReviewedNone } from "./review.js";

test("readReviewStatus returns stage 'none' when no review register exists", () => {
  const status = readReviewStatus(process.cwd(), "LICENSE-DE.md");
  assert.equal(status.slot, "LICENSE-DE.md");
  assert.equal(status.stage, "none");
});

test("allReviewedNone returns 'none' for every slot", () => {
  const statuses = allReviewedNone(process.cwd(), [
    "LICENSE-DE.md",
    "LICENSE-FR.md",
    "LICENSE-SLO.md",
  ]);
  assert.equal(statuses.length, 3);
  for (const s of statuses) {
    assert.equal(s.stage, "none");
  }
});

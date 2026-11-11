import assert from "node:assert/strict";
import { test } from "node:test";
import { readDeedWitnesses, hasAnyDeed } from "./deed.js";

test("readDeedWitnesses returns an array (may be empty when no canon/register)", () => {
  const witnesses = readDeedWitnesses(process.cwd());
  assert.ok(Array.isArray(witnesses));
  for (const w of witnesses) {
    assert.ok(["dokaz", "padec", "lineage"].includes(w.kind));
    assert.ok(["⊢", "⚠"].includes(w.status));
    assert.ok(typeof w.ref === "string" && w.ref.length > 0);
  }
});

test("hasAnyDeed returns a boolean", () => {
  assert.ok(typeof hasAnyDeed(process.cwd()) === "boolean");
});

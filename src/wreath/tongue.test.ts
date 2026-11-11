import assert from "node:assert/strict";
import { test } from "node:test";
import { listTongues, getTongue, tongueFromSlot } from "./tongue.js";

test("listTongues returns every registered wreath tongue", () => {
  const tongues = listTongues();
  assert.ok(tongues.length >= 36, `expected at least 36 tongues, got ${tongues.length}`);
  const codes = tongues.map((t) => t.code);
  assert.ok(codes.includes("DE"), "DE (Nemščina) should be registered");
  assert.ok(codes.includes("EN"), "EN (Angleščina, vir) should be registered");
  assert.ok(codes.includes("SLO"), "SLO (Slovenščina, tla) should be registered");
  assert.ok(codes.includes("JA"), "JA (Japonščina) should be registered");
  assert.ok(codes.includes("ZH"), "ZH (Kitajščina) should be registered");
});

test("getTongue resolves a known code and is case-insensitive", () => {
  const de = getTongue("DE");
  assert.ok(de);
  assert.equal(de.language, "Nemščina");
  assert.equal(de.canon, "Ordnung");
  assert.equal(de.status, "slot");
  assert.equal(getTongue("de"), de, "case-insensitive lookup");
});

test("getTongue returns undefined for unknown code", () => {
  assert.equal(getTongue("XX"), undefined);
});

test("tongueFromSlot maps LICENSE-XX.md to its tongue", () => {
  const fr = tongueFromSlot("LICENSE-FR.md");
  assert.ok(fr);
  assert.equal(fr.code, "FR");
  assert.equal(fr.canon, "Précision");
});

test("tongueFromSlot maps LICENSE.md to the issued door (EN)", () => {
  const en = tongueFromSlot("LICENSE.md");
  assert.ok(en);
  assert.equal(en.code, "EN");
  assert.equal(en.status, "issued");
});

test("every tongue has a 64-hex-free shape and non-empty fields", () => {
  for (const t of listTongues()) {
    assert.ok(t.code.length > 0);
    assert.ok(t.language.length > 0);
    assert.ok(t.slot.startsWith("LICENSE-") || t.slot === "LICENSE.md");
    assert.ok(t.canon.length > 0);
    assert.ok(t.connotation.length > 0);
    assert.ok(t.status === "slot" || t.status === "issued");
  }
});

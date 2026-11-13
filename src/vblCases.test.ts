import assert from "node:assert/strict";
import { appendFile, mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { addAction, addEvidence, createCase, getCase, listCases, recordReview, updateAction } from "./vblCases.js";

test("case workflow uses the canonical review register and capture/seal pipeline", async () => {
  const root = await mkdtemp(join(tmpdir(), "vbl-case-"));
  try {
    const created = await createCase(root, { title: "Review source", claim: "A supplied claim needs checking.", reporter: "Reporter A" });
    assert.equal(created.status, "UNVERIFIED");
    assert.equal(created.integrity.valid, true);

    const evidence = await addEvidence(root, created.id, { label: "Source excerpt", source: "incoming submission", content: "Original evidence bytes", actor: "Reporter A" });
    assert.equal(evidence.evidence.length, 1);
    assert.match(evidence.evidence[0]!.contentHash, /^[a-f0-9]{64}$/);
    assert.equal(evidence.integrity.valid, true);
    const manifest = JSON.parse(await readFile(join(root, "book.workbench.json"), "utf8")) as { incomingTexts: Array<{ id: string; sourcePath: string }> };
    assert.equal(manifest.incomingTexts.length, 2);
    assert.equal(manifest.incomingTexts.find((entry) => entry.id === evidence.events.find((event) => event.type === "evidence.added")!.payload.incomingTextId)?.id, evidence.events.find((event) => event.type === "evidence.added")!.payload.incomingTextId);
    assert.equal(await readFile(join(root, manifest.incomingTexts.find((entry) => entry.id === evidence.events.find((event) => event.type === "evidence.added")!.payload.incomingTextId)!.sourcePath), "utf8"), "Original evidence bytes");

    await assert.rejects(recordReview(root, created.id, { reviewer: "Same", executor: "same", outcome: "SUPPORTED", scope: "source", findings: [] }), /Reviewer must differ/);
    const reviewed = await recordReview(root, created.id, { reviewer: "Reviewer B", executor: "Reporter A", outcome: "SUPPORTED", scope: "source comparison", findings: ["Evidence matches submitted source."] });
    assert.equal(reviewed.status, "SUPPORTED");
    const withAction = await addAction(root, created.id, { description: "Notify reporter of outcome", owner: "Operator C", actor: "Reviewer B" });
    const done = await updateAction(root, created.id, withAction.actions[0]!.id, "DONE", "Operator C");
    assert.equal(done.actions[0]!.status, "DONE");
    assert.equal(done.integrity.valid, true);

    const rows = (await readFile(join(root, "REGISTER-PREVERJANJ.jsonl"), "utf8")).trim().split(/\r?\n/).map((line) => JSON.parse(line) as Record<string, unknown>);
    assert.equal(rows.filter((row) => row.subject === `case:${created.id}`).length, 5);
    assert.equal((await listCases(root)).length, 1);
    assert.equal((await getCase(root, created.id))?.events.length, 5);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("tampering with a stored case event is detected", async () => {
  const root = await mkdtemp(join(tmpdir(), "vbl-case-tamper-"));
  try {
    const created = await createCase(root, { title: "Integrity", claim: "Claim", reporter: "A" });
    const register = join(root, "REGISTER-PREVERJANJ.jsonl");
    const line = JSON.parse((await readFile(register, "utf8")).trim()) as { case_event: { payload: Record<string, unknown> } };
    line.case_event.payload.claim = "silently changed";
    await appendFile(register, `${JSON.stringify({ ...line, subject: "tamper-copy" })}\n`, "utf8");
    const reloaded = await getCase(root, created.id);
    assert.equal(reloaded?.integrity.valid, false);
    assert.ok(reloaded?.integrity.errors.some((error) => error.includes("event hash mismatch")));
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

import { createHash, randomUUID } from "node:crypto";
import { appendFile, readFile } from "node:fs/promises";
import { join } from "node:path";
import { captureIncomingText } from "./workbenchManifestRepository.js";

export type ClaimStatus = "UNVERIFIED" | "SUPPORTED" | "DISPUTED" | "INCONCLUSIVE";
export type ReviewOutcome = Exclude<ClaimStatus, "UNVERIFIED">;
export type CaseEventType = "case.created" | "evidence.added" | "review.recorded" | "action.created" | "action.updated";
export type CaseEventInput = { caseId: string; type: CaseEventType; actor: string; payload: Record<string, unknown> };

export interface CaseEvent {
  eventId: string; caseId: string; sequence: number; type: CaseEventType; occurredAt: string;
  actor: string; previousHash: string | null; payload: Record<string, unknown>; hash: string;
}
export interface VblCase {
  id: string; title: string; claim: string; reporter: string; status: ClaimStatus; createdAt: string;
  latestReview?: { reviewer: string; executor: string; outcome: ReviewOutcome; scope: string; findings: string[]; eventId: string };
  evidence: Array<{ id: string; label: string; source: string; contentHash: string; addedBy: string; eventId: string }>;
  actions: Array<{ id: string; description: string; owner: string; status: "OPEN" | "DONE"; eventId: string }>;
  events: CaseEvent[]; integrity: { valid: boolean; errors: string[] };
}

const REGISTER_FILE = "REGISTER-PREVERJANJ.jsonl";
let writeQueue: Promise<void> = Promise.resolve();

export async function listCases(projectRoot: string): Promise<VblCase[]> {
  const events = await readCaseEvents(projectRoot);
  return [...new Set(events.map((event) => event.caseId))].map((id) => buildCase(id, events.filter((event) => event.caseId === id)));
}
export async function getCase(projectRoot: string, caseId: string): Promise<VblCase | null> {
  const events = (await readCaseEvents(projectRoot)).filter((event) => event.caseId === caseId);
  return events.length ? buildCase(caseId, events) : null;
}
export async function createCase(projectRoot: string, input: { title: string; claim: string; reporter: string }): Promise<VblCase> {
  const title = required("title", input.title), claim = required("claim", input.claim), reporter = required("reporter", input.reporter);
  const caseId = randomUUID();
  const captured = await captureIncomingText(projectRoot, { title: `Case ${caseId}: claim`, body: claim, note: "Original claim text; case intake." });
  await appendCaseEvent(projectRoot, { caseId, type: "case.created", actor: reporter, payload: { title, claim, reporter, incomingTextId: captured.value.id, sourcePath: captured.value.sourcePath } });
  return (await getCase(projectRoot, caseId))!;
}
export async function addEvidence(projectRoot: string, caseId: string, input: { label: string; source: string; content: string; actor: string }): Promise<VblCase> {
  const label = required("label", input.label), source = required("source", input.source), content = required("content", input.content), actor = required("actor", input.actor);
  requireCase(await getCase(projectRoot, caseId), caseId);
  const captured = await captureIncomingText(projectRoot, { title: `Case ${caseId}: ${label}`, body: content, note: `Evidence source: ${source}` });
  await appendCaseEvent(projectRoot, { caseId, type: "evidence.added", actor, payload: {
    evidenceId: randomUUID(), label, source, incomingTextId: captured.value.id,
    sourcePath: captured.value.sourcePath, contentHash: createHash("sha256").update(content, "utf8").digest("hex"),
  } });
  return (await getCase(projectRoot, caseId))!;
}
export async function recordReview(projectRoot: string, caseId: string, input: { reviewer: string; executor: string; outcome: ReviewOutcome; scope: string; findings: string[] }): Promise<VblCase> {
  const reviewer = required("reviewer", input.reviewer), executor = required("executor", input.executor), scope = required("scope", input.scope);
  requireCase(await getCase(projectRoot, caseId), caseId);
  if (reviewer.toLocaleLowerCase() === executor.toLocaleLowerCase()) throw new Error("Reviewer must differ from executor.");
  if (!["SUPPORTED", "DISPUTED", "INCONCLUSIVE"].includes(input.outcome)) throw new Error("Invalid review outcome.");
  if (!Array.isArray(input.findings) || input.findings.some((finding) => typeof finding !== "string")) throw new Error("findings must be an array of strings.");
  const priorEvidence = (await getCase(projectRoot, caseId))!.evidence;
  await appendCaseEvent(projectRoot, { caseId, type: "review.recorded", actor: reviewer, payload: { reviewer, executor, outcome: input.outcome, scope, findings: input.findings, evidenceIds: priorEvidence.map((item) => item.id) } });
  return (await getCase(projectRoot, caseId))!;
}
export async function addAction(projectRoot: string, caseId: string, input: { description: string; owner: string; actor: string }): Promise<VblCase> {
  const description = required("description", input.description), owner = required("owner", input.owner), actor = required("actor", input.actor);
  requireCase(await getCase(projectRoot, caseId), caseId);
  await appendCaseEvent(projectRoot, { caseId, type: "action.created", actor, payload: { actionId: randomUUID(), description, owner, status: "OPEN" } });
  return (await getCase(projectRoot, caseId))!;
}
export async function updateAction(projectRoot: string, caseId: string, actionId: string, status: "OPEN" | "DONE", actor: string): Promise<VblCase> {
  required("actor", actor);
  const current = requireCase(await getCase(projectRoot, caseId), caseId);
  if (!current.actions.some((action) => action.id === actionId)) throw new Error(`Action not found: ${actionId}`);
  if (status !== "OPEN" && status !== "DONE") throw new Error("Invalid action status.");
  await appendCaseEvent(projectRoot, { caseId, type: "action.updated", actor, payload: { actionId, status } });
  return (await getCase(projectRoot, caseId))!;
}

export async function appendCaseEvent(projectRoot: string, input: CaseEventInput): Promise<void> {
  const caseId = required("caseId", input.caseId), actor = required("actor", input.actor);
  const operation = writeQueue.then(async () => {
    const events = (await readCaseEvents(projectRoot)).filter((event) => event.caseId === caseId);
    if (!events.length && input.type !== "case.created") throw new Error(`Case not found: ${caseId}`);
    if (events.length && input.type === "case.created") throw new Error(`Case already exists: ${caseId}`);
    const prev = events.at(-1);
    const unsigned = { eventId: randomUUID(), caseId, sequence: events.length + 1, type: input.type, occurredAt: new Date().toISOString(), actor, previousHash: prev?.hash ?? null, payload: input.payload };
    const event: CaseEvent = { ...unsigned, hash: hashEvent(unsigned) };
    const row = {
      claim_id: `CASE-${caseId}-${String(event.sequence).padStart(6, "0")}`,
      subject: `case:${caseId}`,
      claim: input.type === "case.created" ? String(input.payload.claim ?? "Case created") : `${input.type} for case ${caseId}`,
      witnesses: Array.isArray(input.payload.evidenceIds) ? input.payload.evidenceIds : (typeof input.payload.sourcePath === "string" ? [input.payload.sourcePath] : []),
      method: input.type,
      result: input.type === "review.recorded" ? input.payload.outcome : "UNVERIFIED",
      reviewer: actor, timestamp: event.occurredAt,
      limitations: "Operational record; not proof of identity, truth, legal effect, or delivery.", case_event: event,
    };
    await appendFile(join(projectRoot, REGISTER_FILE), `${JSON.stringify(row)}\n`, "utf8");
  });
  writeQueue = operation.catch(() => undefined);
  await operation;
}

export async function readCaseEvents(projectRoot: string): Promise<CaseEvent[]> {
  let text: string;
  try { text = await readFile(join(projectRoot, REGISTER_FILE), "utf8"); }
  catch (error) { if ((error as NodeJS.ErrnoException).code === "ENOENT") return []; throw error; }
  const events: CaseEvent[] = [];
  for (const [index, line] of text.split(/\r?\n/).entries()) {
    if (!line.trim()) continue;
    let row: Record<string, unknown>;
    try { row = JSON.parse(line) as Record<string, unknown>; } catch { throw new Error(`Claim/evidence register JSON invalid at line ${index + 1}.`); }
    if (row.case_event && typeof row.case_event === "object") events.push(row.case_event as CaseEvent);
  }
  return events;
}

function buildCase(id: string, events: CaseEvent[]): VblCase {
  const errors: string[] = [];
  let prev: string | null = null;
  events.forEach((event, i) => {
    if (event.sequence !== i + 1) errors.push(`sequence mismatch at event ${i + 1}`);
    if (event.previousHash !== prev) errors.push(`previous hash mismatch at event ${i + 1}`);
    if (event.hash !== hashEvent({ eventId: event.eventId, caseId: event.caseId, sequence: event.sequence, type: event.type, occurredAt: event.occurredAt, actor: event.actor, previousHash: event.previousHash, payload: event.payload })) errors.push(`event hash mismatch at event ${i + 1}`);
    prev = event.hash;
  });
  const created = events.find((event) => event.type === "case.created");
  if (!created) throw new Error(`Case ${id} has no creation event.`);
  const p = created.payload, evidence: VblCase["evidence"] = [], actions = new Map<string, VblCase["actions"][number]>();
  let latestReview: VblCase["latestReview"], status: ClaimStatus = "UNVERIFIED";
  for (const event of events) {
    if (event.type === "evidence.added") evidence.push({ id: String(event.payload.evidenceId), label: String(event.payload.label), source: String(event.payload.source), contentHash: String(event.payload.contentHash), addedBy: event.actor, eventId: event.eventId });
    if (event.type === "review.recorded") { latestReview = { reviewer: String(event.payload.reviewer), executor: String(event.payload.executor), outcome: event.payload.outcome as ReviewOutcome, scope: String(event.payload.scope), findings: event.payload.findings as string[], eventId: event.eventId }; status = latestReview.outcome; }
    if (event.type === "action.created") actions.set(String(event.payload.actionId), { id: String(event.payload.actionId), description: String(event.payload.description), owner: String(event.payload.owner), status: "OPEN", eventId: event.eventId });
    if (event.type === "action.updated") { const action = actions.get(String(event.payload.actionId)); if (action && (event.payload.status === "OPEN" || event.payload.status === "DONE")) actions.set(action.id, { ...action, status: event.payload.status, eventId: event.eventId }); }
  }
  return { id, title: String(p.title), claim: String(p.claim), reporter: String(p.reporter), status, createdAt: created.occurredAt, ...(latestReview ? { latestReview } : {}), evidence, actions: [...actions.values()], events, integrity: { valid: !errors.length, errors } };
}
function hashEvent(event: Omit<CaseEvent, "hash">): string { return createHash("sha256").update(canonicalJson(event), "utf8").digest("hex"); }
function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") { const r = value as Record<string, unknown>; return `{${Object.keys(r).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(r[key])}`).join(",")}}`; }
  return JSON.stringify(value);
}
function required(name: string, value: unknown): string { if (typeof value !== "string" || !value.trim()) throw new Error(`${name} must be a non-empty string.`); return value.trim(); }
function requireCase(value: VblCase | null, id: string): VblCase { if (!value) throw new Error(`Case not found: ${id}`); return value; }

import { useEffect, useState, type FormEvent } from "react";
import type { VblCase } from "../types";
import { tauriApi, workbenchApi } from "../api";
import { BundleToolsPanel } from "./BundleToolsPanel";

export function VblCasesPanel({ projectRoot }: { projectRoot: string | null }) {
  const [cases, setCases] = useState<VblCase[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [title, setTitle] = useState("");
  const [claim, setClaim] = useState("");
  const [reporter, setReporter] = useState("");
  const [label, setLabel] = useState("");
  const [source, setSource] = useState("");
  const [content, setContent] = useState("");
  const [reviewer, setReviewer] = useState("");
  const [executor, setExecutor] = useState("");
  const [scope, setScope] = useState("");
  const [outcome, setOutcome] = useState<"SUPPORTED" | "DISPUTED" | "INCONCLUSIVE">("SUPPORTED");
  const [findings, setFindings] = useState("");
  const [actionText, setActionText] = useState("");
  const [actionOwner, setActionOwner] = useState("");
  const [error, setError] = useState("");

  const desktop = Boolean((window as Window & { __TAURI_INTERNALS__?: unknown }).__TAURI_INTERNALS__);
  async function refresh() {
    if (!projectRoot) { setCases([]); setSelectedId(""); return; }
    const items = desktop ? await tauriApi.listCases(projectRoot) : await workbenchApi.getVblCases();
    setCases(items);
    setSelectedId((current) => current && items.some((item) => item.id === current) ? current : items[0]?.id ?? "");
  }
  useEffect(() => { if (projectRoot) void refresh().catch((err: unknown) => setError(err instanceof Error ? err.message : "Could not load cases.")); }, [projectRoot, desktop]);
  const selected = cases.find((item) => item.id === selectedId);

  async function run(operation: () => Promise<VblCase | VblCase[]>) {
    setError("");
    try { const result = await operation(); if (Array.isArray(result)) setCases(result); else { setCases((all) => [result, ...all.filter((item) => item.id !== result.id)]); setSelectedId(result.id); } await refresh(); }
    catch (err) { setError(err instanceof Error ? err.message : "Operation failed."); }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await run(() => desktop ? tauriApi.createCase(projectRoot!, { title, claim, reporter }) : workbenchApi.createVblCase({ title, claim, reporter }));
    setTitle(""); setClaim("");
  }
  const actor = reviewer.trim() || reporter.trim() || "local-operator";

  if (!projectRoot) return <section className="case-workbench"><header className="case-heading"><div><p className="eyebrow">VBL · EVIDENCE & ACTION</p><h2>Case ledger</h2><p>Select a project folder to keep case records and evidence on that folder.</p></div></header></section>;

  return <section className="case-workbench">
    <header className="case-heading"><div><p className="eyebrow">VBL · EVIDENCE & ACTION</p><h2>Case ledger</h2><p>Claims move through evidence, review, action, and re-check. Hashes verify bytes, not truth.</p></div><span className="case-count">{cases.length} cases</span></header>
    {error && <p className="case-error" role="alert">{error}</p>}
    <div className="case-grid">
      <aside className="case-sidebar">
        <form className="case-form" onSubmit={submit}><h3>Open a case</h3>
          <label>Case title<input required value={title} onChange={(e) => setTitle(e.target.value)} /></label>
          <label>Claim or signal<textarea required rows={3} value={claim} onChange={(e) => setClaim(e.target.value)} /></label>
          <label>Reporter<input required value={reporter} onChange={(e) => setReporter(e.target.value)} /></label>
          <button className="primary-button" type="submit">Open case</button>
        </form>
        <ul className="case-list">{cases.map((item) => <li key={item.id}><button className={item.id === selectedId ? "case-select selected" : "case-select"} onClick={() => setSelectedId(item.id)}><strong>{item.title}</strong><span>{item.status} · {item.evidence.length} evidence</span></button></li>)}</ul>
      </aside>
      <div className="case-main">{!selected ? <p className="empty">Open or select a case to begin its evidence trail.</p> : <>
        <div className="case-title-row"><div><p className="eyebrow">{selected.id}</p><h3>{selected.title}</h3></div><span className={`case-status ${selected.status.toLowerCase()}`}>{selected.status}</span></div>
        <blockquote>{selected.claim}</blockquote>
        <div className={selected.integrity.valid ? "integrity-ok" : "integrity-fail"}>Event chain {selected.integrity.valid ? "verified" : "BROKEN"} · {selected.events.length} events · SHA-256 links detect edits, not authorship.</div>
        {selected.integrity.errors.length > 0 && <ul>{selected.integrity.errors.map((e) => <li key={e}>{e}</li>)}</ul>}
        <div className="case-workflow">
          <form className="case-form" onSubmit={(e) => { e.preventDefault(); void run(() => desktop ? tauriApi.addCaseEvidence(projectRoot!, selected.id, { label, source, content, actor: reporter || "local-operator" }) : workbenchApi.addVblEvidence(selected.id, { label, source, content, actor: reporter || "local-operator" })); setLabel(""); setSource(""); setContent(""); }}><h4>1 · Attach evidence</h4>
            <label>Label<input required value={label} onChange={(e) => setLabel(e.target.value)} /></label><label>Source / location<input required value={source} onChange={(e) => setSource(e.target.value)} /></label><label>Evidence text<textarea required rows={3} value={content} onChange={(e) => setContent(e.target.value)} /></label><button type="submit">Hash and attach evidence</button>
          </form>
          <form className="case-form" onSubmit={(e) => { e.preventDefault(); void run(() => desktop ? tauriApi.recordCaseReview(projectRoot!, selected.id, { reviewer, executor, scope, outcome, findings: findings.split("\n").map((x) => x.trim()).filter(Boolean) }) : workbenchApi.recordVblReview(selected.id, { reviewer, executor, scope, outcome, findings: findings.split("\n").map((x) => x.trim()).filter(Boolean) })); }}><h4>2 · Independent review</h4>
            <label>Reviewer<input required value={reviewer} onChange={(e) => setReviewer(e.target.value)} /></label><label>Executor<input required value={executor} onChange={(e) => setExecutor(e.target.value)} /></label><label>Review scope<input required value={scope} onChange={(e) => setScope(e.target.value)} /></label><label>Outcome<select value={outcome} onChange={(e) => setOutcome(e.target.value as typeof outcome)}><option value="SUPPORTED">Supported</option><option value="DISPUTED">Disputed</option><option value="INCONCLUSIVE">Inconclusive</option></select></label><label>Findings, one per line<textarea rows={2} value={findings} onChange={(e) => setFindings(e.target.value)} /></label><button type="submit">Record review</button>
          </form>
          <form className="case-form" onSubmit={(e) => { e.preventDefault(); void run(() => desktop ? tauriApi.addCaseAction(projectRoot!, selected.id, { description: actionText, owner: actionOwner, actor }) : workbenchApi.addVblAction(selected.id, { description: actionText, owner: actionOwner, actor })); setActionText(""); }}><h4>3 · Assign follow-up</h4><label>Action<input required value={actionText} onChange={(e) => setActionText(e.target.value)} /></label><label>Owner<input required value={actionOwner} onChange={(e) => setActionOwner(e.target.value)} /></label><button type="submit">Add action</button></form>
        </div>
        <h4>Evidence</h4><ul className="case-records">{selected.evidence.map((item) => <li key={item.id}><strong>{item.label}</strong> · {item.source}<code>{item.contentHash}</code></li>)}</ul>
        <h4>Actions</h4><ul className="case-records">{selected.actions.map((item) => <li key={item.id}><strong>{item.status}</strong> · {item.description} · owner: {item.owner}{item.status === "OPEN" && <button onClick={() => void run(() => desktop ? tauriApi.updateCaseAction(projectRoot!, selected.id, item.id, "DONE", actor) : workbenchApi.updateVblAction(selected.id, item.id, "DONE", actor))}>Mark done</button>}</li>)}</ul>
        <h4>Append-only event trail</h4><ol className="case-events">{[...selected.events].reverse().map((event) => <li key={event.eventId}><strong>{event.type}</strong><span>{event.occurredAt} · {event.actor}</span><code>{event.hash}</code></li>)}</ol>
      </>}</div>
    </div>
    {desktop && <BundleToolsPanel projectRoot={projectRoot} cases={cases} onImported={refresh} />}
  </section>;
}

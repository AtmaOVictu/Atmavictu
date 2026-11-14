import { useEffect, useState } from "react";
import type { BundlePreview, VblCase } from "../types";
import { tauriApi } from "../api";

function summary(p: BundlePreview): string { return `${p.valid ? "PASS" : "FAIL"} · ${p.fileCount} files · ${p.caseCount} cases${p.caseIds.length ? ` · ${p.caseIds.join(", ")}` : ""}${p.errors.length ? ` · ${p.errors.join("; ")}` : ""}`; }

export function BundleToolsPanel({ projectRoot, cases, onImported }: { projectRoot: string; cases: VblCase[]; onImported: () => Promise<void> }) {
  const [caseId, setCaseId] = useState("");
  const [path, setPath] = useState("");
  const [target, setTarget] = useState("");
  const [preview, setPreview] = useState<BundlePreview | null>(null);
  const [overwrite, setOverwrite] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const run = async (fn: () => Promise<void>) => { setBusy(true); setMessage(""); try { await fn(); } catch (e) { setMessage(e instanceof Error ? e.message : "Bundle operation failed."); } finally { setBusy(false); } };

  useEffect(() => { if (!cases.some(item => item.id === caseId)) setCaseId(cases[0]?.id ?? ""); }, [cases, caseId]);

  return <section className="case-workbench bundle-tools">
    <header className="case-heading"><div><p className="eyebrow">LOCAL · OFFLINE</p><h2>Backup &amp; case exchange</h2><p>Bundles remain on this device. Import and restore require integrity preview and confirmation.</p></div></header>
    <div className="bundle-actions">
      <button disabled={busy} onClick={() => void run(async () => { const dest = await tauriApi.saveBundlePath("atmavictu-project-backup.json"); if (!dest) return; const result = await tauriApi.exportProjectBackup(projectRoot, dest); setPath(dest); setPreview(result); setMessage(`Project backup saved: ${dest} · ${summary(result)}`); })}>Create full project backup</button>
      <label>Case to export<select value={caseId} onChange={e => setCaseId(e.target.value)}><option value="">Select case</option>{cases.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}</select></label>
      <button disabled={busy || !caseId} onClick={() => void run(async () => { const dest = await tauriApi.saveBundlePath(`case-${caseId}.json`); if (!dest) return; const result = await tauriApi.exportCaseBundle(projectRoot, caseId, dest); setPath(dest); setPreview(result); setMessage(`Case export saved: ${dest} · ${summary(result)}`); })}>Export selected case</button>
      <button disabled={busy} onClick={() => void run(async () => { const selected = await tauriApi.openBundleFile(); if (!selected) return; const result = await tauriApi.previewBackup(selected); setPath(selected); setPreview(result); setOverwrite(false); setMessage(`Preview: ${summary(result)}`); })}>Choose bundle · preview</button>
    </div>
    {preview && <div className={preview.valid ? "integrity-ok" : "integrity-fail"}><code>{path}</code><p>{summary(preview)}</p>
      {preview.valid && preview.format === "atmavictu-case-bundle-v1" && <button disabled={busy} onClick={() => void run(async () => { if (!window.confirm(`Import ${preview.caseCount} case(s)? Existing case IDs are refused.`)) return; const result = await tauriApi.importCaseBundle(projectRoot, path); setPreview(result); await onImported(); setMessage(`Case import complete · ${summary(result)}`); })}>Confirm case import</button>}
      {preview.valid && preview.format === "atmavictu-project-bundle-v1" && <>
        <div className="bundle-actions"><input aria-label="Restore destination folder" readOnly value={target} placeholder="Choose restore destination"/><button disabled={busy} onClick={() => void run(async () => { const selected = await tauriApi.openFolderPath(); if (selected) setTarget(selected); })}>Choose folder</button></div>
        <label><input type="checkbox" checked={overwrite} onChange={e => setOverwrite(e.target.checked)}/> Allow replacing existing files</label>
        <button disabled={busy || !target} onClick={() => void run(async () => { if (!window.confirm(`Restore verified backup into ${target}?`)) return; const result = await tauriApi.restoreBackup(path, target, overwrite); setPreview(result); setMessage(`Restore complete · ${summary(result)}`); })}>Confirm project restore</button>
      </>}
    </div>}
    {message && <p role="status">{message}</p>}
  </section>;
}

import { useEffect, useState } from "react";
import type { BundlePreview } from "../types";
import { tauriApi } from "../api";


function describe(preview: BundlePreview): string {
  return `${preview.valid ? "Integrity preview passed" : "Integrity preview failed"}: ${preview.fileCount} files, ${preview.caseCount} cases${preview.caseIds.length ? ` (${preview.caseIds.join(", ")})` : ""}${preview.errors.length ? `; ${preview.errors.join("; ")}` : ""}`;
}

export function BundleToolsPanel({ projectRoot }: { projectRoot: string | null }) {
  const [preview, setPreview] = useState<BundlePreview | null>(null);
  const [previewPath, setPreviewPath] = useState("");
  const [overwrite, setOverwrite] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [caseId, setCaseId] = useState("");
  const [cases, setCases] = useState<Array<{ id: string; title: string }>>([]);
  const desktop = Boolean((window as Window & { __TAURI_INTERNALS__?: unknown }).__TAURI_INTERNALS__);
  useEffect(() => { if (!projectRoot || !desktop) { setCaseId(""); setCases([]); return; } void tauriApi.listCases(projectRoot).then(items => { setCases(items); setCaseId(current => current || items[0]?.id || ""); }).catch(() => undefined); }, [projectRoot, desktop]);

  async function run(operation: () => Promise<void>) {
    setBusy(true); setMessage("");
    try { await operation(); } catch (error) { setMessage(error instanceof Error ? error.message : "Local bundle operation failed."); }
    finally { setBusy(false); }
  }
  async function chooseBundle(): Promise<string | null> {
    return tauriApi.openBundleFile();
  }

  return <section className="case-workbench bundle-tools">
    <header className="case-heading"><div><p className="eyebrow">LOCAL FILES ONLY</p><h2>Backup &amp; case exchange</h2><p>Bundles stay on your device. Verify the preview before restoring or importing.</p></div></header>
    {!projectRoot && <p className="empty">Select a project folder to enable local bundles.</p>}
    {!desktop && <p className="empty">Portable bundles are available in the desktop app; case operations in browser mode remain on the existing API.</p>}
    {desktop && projectRoot && <label>Case to export<select value={caseId} onChange={e => setCaseId(e.target.value)}><option value="">Select case</option>{cases.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}</select></label>}
    <div className="bundle-actions">
      <button disabled={!projectRoot || busy} onClick={() => void run(async () => {
        const path = await tauriApi.saveBundlePath("atmavictu-project-backup.json");
        if (!path) return;
        const result = await tauriApi.exportProjectBackup(projectRoot!, path);
        setPreview(result); setPreviewPath(path); setMessage(`Backup written locally: ${path}. ${describe(result)}`);
      })}>Create full project backup</button>
      <button disabled={!projectRoot || busy} onClick={() => void run(async () => {
        if (!caseId) throw new Error("Select a case before exporting it.");
        const path = await tauriApi.saveBundlePath(`case-${caseId}.json`);
        if (!path) return;
        const result = await tauriApi.exportCaseBundle(projectRoot!, caseId, path);
        setPreview(result); setPreviewPath(path); setMessage(`Case bundle written locally: ${path}. ${describe(result)}`);
      })}>Export selected case</button>
      <button disabled={!projectRoot || busy} onClick={() => void run(async () => {
        const path = await chooseBundle(); if (!path) return;
        const result = await tauriApi.previewBundle(path);
        setPreview(result); setPreviewPath(path); setOverwrite(false); setMessage(describe(result));
      })}>Choose bundle and preview</button>
    </div>
    {preview && <div className={preview.valid ? "integrity-ok" : "integrity-fail"}>
      <strong>{previewPath}</strong><p>{describe(preview)}</p>
      {preview.valid && projectRoot && <>
        <button disabled={busy} onClick={() => void run(async () => {
          if (preview.caseCount > 0) {
            const accepted = window.confirm(`Import ${preview.caseCount} case(s) into this project? Existing case IDs are not merged.`);
            if (!accepted) return;
            const result = await tauriApi.importCaseBundle(projectRoot, previewPath); setPreview(result); setMessage(`Case import completed. ${describe(result)}`);
          } else {
            const accepted = window.confirm(`Restore ${preview.fileCount} files? This may replace project files.`);
            if (!accepted) return;
            const result = await tauriApi.restoreProjectBackup(previewPath, projectRoot, overwrite); setPreview(result); setMessage(`Project restore completed. ${describe(result)}`);
          }
        })}>{preview.caseCount > 0 ? "Confirm case import" : "Restore full backup"}</button>
        {preview.caseCount === 0 && <label className="overwrite-option"><input type="checkbox" checked={overwrite} onChange={(e) => setOverwrite(e.target.checked)} /> Allow replacing existing files</label>}
      </>}
    </div>}
    {message && <p role="status">{message}</p>}
  </section>;
}

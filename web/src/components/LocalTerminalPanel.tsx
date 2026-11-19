import { useState, type FormEvent } from "react";
import type { WorkbenchManifest } from "../types";
import { tauriApi, workbenchApi } from "../api";

type Entry = { command: string; output: string; status: "PASS" | "FAIL" | "INFO" };
const tokens = (text: string) => new Set(text.toLocaleLowerCase().match(/[\p{L}\p{N}]+/gu) ?? []);
const overlap = (a: Set<string>, b: Set<string>) => [...a].filter((word) => word.length > 2 && b.has(word)).length;

export function LocalTerminalPanel({ projectRoot, manifest }: { projectRoot: string | null; manifest: WorkbenchManifest | null }) {
  const [command, setCommand] = useState("");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [busy, setBusy] = useState(false);
  const desktop = Boolean((window as Window & { __TAURI_INTERNALS__?: unknown }).__TAURI_INTERNALS__);

  async function submit(event: FormEvent) {
    event.preventDefault();
    const input = command.trim();
    if (!input) return;
    setCommand(""); setBusy(true);
    let entry: Entry;
    try {
      const [verb, ...args] = input.split(/\s+/);
      if (verb === "help") {
        entry = { command: input, status: "INFO", output: "Local commands: help · status · verify · cases · describe <text> · backup <file.json> · export-case <case-id> <file.json>. No arbitrary shell execution or network model calls." };
      } else if (verb === "status") {
        entry = { command: input, status: "PASS", output: `Project: ${projectRoot ?? "not selected"}\nManifest intake: ${manifest?.incomingTexts.length ?? 0}\nFragments: ${manifest?.fragments.length ?? 0}\nCases: ${desktop && projectRoot ? (await tauriApi.listCases(projectRoot)).length : "desktop case listing unavailable"}` };
      } else if (verb === "verify") {
        if (!projectRoot) throw new Error("Select a project folder first.");
        const result = desktop ? await tauriApi.verifyManifest(projectRoot) : await workbenchApi.getVerify();
        entry = { command: input, status: result.isValid ? "PASS" : "FAIL", output: result.isValid ? "Manifest structure checks passed." : result.errors.join("\n") };
      } else if (verb === "cases") {
        if (!desktop || !projectRoot) throw new Error("Case listing requires the desktop app and a selected folder.");
        const all = await tauriApi.listCases(projectRoot);
        entry = { command: input, status: "PASS", output: all.length ? all.map((item) => `${item.id} · ${item.status} · ${item.title}`).join("\n") : "No cases recorded." };
      } else if (verb === "describe") {
        const text = input.slice("describe".length).trim();
        if (!text) throw new Error("Usage: describe <text>");
        const words = tokens(text);
        const counts = new Map<string, number>();
        for (const word of text.toLocaleLowerCase().match(/[\p{L}\p{N}]+/gu) ?? []) counts.set(word, (counts.get(word) ?? 0) + 1);
        const frequent = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 8).map(([word, count]) => `${word} (${count})`);
        const concepts = (manifest?.concepts ?? []).map((concept) => ({ label: concept.label, score: overlap(words, tokens(`${concept.label} ${concept.note ?? ""}`)) })).filter((item) => item.score > 0).sort((a, b) => b.score - a.score).slice(0, 5);
        const related = (manifest?.fragments ?? []).map((fragment) => ({ title: fragment.title ?? fragment.id, score: overlap(words, tokens(`${fragment.title ?? ""} ${fragment.text}`)), text: fragment.text })).filter((item) => item.score > 0).sort((a, b) => b.score - a.score).slice(0, 3);
        const actionable = /\b(should|must|can|use|apply|implement|build|measure|test|treba|mora|lahko|uporabi|izvedi|preizkusi|izmeri)\b/i.test(text);
        entry = { command: input, status: "INFO", output: [
          `Text: ${text.length} characters · ${[...words].length} unique terms.`,
          `Frequent terms: ${frequent.join(", ") || "none"}.`,
          `Related project concepts: ${concepts.length ? concepts.map((item) => `${item.label} (${item.score} shared terms)`).join("; ") : "no lexical match in saved concepts"}.`,
          `Related saved fragments: ${related.length ? related.map((item) => `${item.title} (${item.score} shared terms): ${item.text.slice(0, 180)}`).join("\n") : "no lexical match in saved fragments"}.`,
          `Applicative signal: ${actionable ? "contains action-oriented terms" : "no explicit action cue detected"}. Next checks: identify the intended beneficiary, required inputs, measurable outcome, constraints, and evidence needed to test it.`,
          "Method boundary: local lexical overlap and rule-based cues only; this does not establish intent, truth, causality, legal meaning, or a verified interpretation. Text is not sent to a model.",
        ].join("\n") };
      } else if (verb === "backup") {
        if (!desktop || !projectRoot) throw new Error("Usage: backup <file.json> requires desktop and a project.");
        const destination = args.join(" ");
        if (!destination) throw new Error("Usage: backup <file.json>");
        const result = await tauriApi.exportProjectBackup(projectRoot, destination);
        entry = { command: input, status: result.valid ? "PASS" : "FAIL", output: `Backup ${destination}\n${result.fileCount} files; ${result.caseCount} cases. ${result.errors.join("; ")}` };
      } else if (verb === "export-case") {
        if (!desktop || !projectRoot || args.length < 2) throw new Error("Usage: export-case <case-id> <file.json>");
        const destination = args.slice(1).join(" ");
        const result = await tauriApi.exportCaseBundle(projectRoot, args[0]!, destination);
        entry = { command: input, status: result.valid ? "PASS" : "FAIL", output: `Case export: ${destination}\n${result.fileCount} files. ${result.errors.join("; ")}` };
      } else {
        throw new Error("Unknown local command. Type help.");
      }
    } catch (error) {
      entry = { command: input, status: "FAIL", output: error instanceof Error ? error.message : "Command failed." };
    }
    setEntries((previous) => [entry, ...previous]); setBusy(false);
  }

  return <section className="case-workbench terminal-panel"><header className="case-heading"><div><p className="eyebrow">LOCAL COMMAND SURFACE · ALLOWLIST ONLY</p><h2>Workbench terminal</h2><p>No shell pass-through; text analysis compares only against saved project material.</p></div></header><form className="terminal-form" onSubmit={submit}><span aria-hidden="true">›</span><input aria-label="Workbench command" value={command} disabled={busy} onChange={(event) => setCommand(event.target.value)} placeholder="help, status, verify, describe text…"/><button type="submit" disabled={busy}>Run</button></form><ol className="terminal-output">{entries.map((item, index) => <li key={`${index}-${item.command}`} className={`terminal-${item.status.toLowerCase()}`}><code>$ {item.command}</code><pre>{item.output}</pre></li>)}</ol></section>;
}

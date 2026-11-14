import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import { readTextFile, writeTextFile } from "@tauri-apps/plugin-fs";
import type {
  Concept,
  ConceptWithCount,
  ExtraLibraryEntry,
  Fragment,
  IncomingText,
  Insertion,
  LibraryEntry,
  ManifestValidationResult,
  Overview,
  SourceAnalysis,
  TreeEntry,
  WreathReport,
  WreathVerification,
  WreathDriftResult,
  WorkbenchManifest,
  VblCase,
} from "./types";

export interface BundlePreview { format: string; valid: boolean; errors: string[]; fileCount: number; caseCount: number; caseIds: string[] }

export interface ManifestSeal {
  manifest_path: string;
  manifest_sha256: string;
  receipts: unknown;
  clock: unknown;
}

export class WorkbenchApiError extends Error {}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: { "content-type": "application/json", ...init?.headers },
  });
  const payload = (await response.json()) as unknown;

  if (!response.ok) {
    const message = isErrorPayload(payload) ? payload.error : `Request failed: ${path}`;
    throw new WorkbenchApiError(message);
  }

  return payload as T;
}

function isErrorPayload(value: unknown): value is { error: string } {
  return typeof value === "object" && value !== null && typeof (value as { error?: unknown }).error === "string";
}

export const workbenchApi = {
  getProject: () => request<{ projectRoot: string }>("/api/project"),
  selectProject: (projectRoot: string) => request<{ projectRoot: string }>("/api/project", { method: "POST", body: JSON.stringify({ projectRoot }) }),
  getVblCases: () => request<VblCase[]>("/api/vbl/cases"),
  createVblCase: (input: { title: string; claim: string; reporter: string }) => request<VblCase>("/api/vbl/cases", { method: "POST", body: JSON.stringify(input) }),
  addVblEvidence: (id: string, input: { label: string; source: string; content: string; actor: string }) => request<VblCase>(`/api/vbl/cases/${encodeURIComponent(id)}/evidence`, { method: "POST", body: JSON.stringify(input) }),
  recordVblReview: (id: string, input: { reviewer: string; executor: string; outcome: "SUPPORTED" | "DISPUTED" | "INCONCLUSIVE"; scope: string; findings: string[] }) => request<VblCase>(`/api/vbl/cases/${encodeURIComponent(id)}/reviews`, { method: "POST", body: JSON.stringify(input) }),
  addVblAction: (id: string, input: { description: string; owner: string; actor: string }) => request<VblCase>(`/api/vbl/cases/${encodeURIComponent(id)}/actions`, { method: "POST", body: JSON.stringify(input) }),
  updateVblAction: (id: string, actionId: string, status: "OPEN" | "DONE", actor: string) => request<VblCase>(`/api/vbl/cases/${encodeURIComponent(id)}/actions/${encodeURIComponent(actionId)}`, { method: "POST", body: JSON.stringify({ status, actor }) }),
  getManifest: () => request<WorkbenchManifest>("/api/manifest"),
  getVerify: () => request<ManifestValidationResult>("/api/verify"),
  getLibrary: () => request<LibraryEntry[]>("/api/library"),
  getLibraryContent: (path: string) =>
    request<{ path: string; content: string }>(`/api/library/content?path=${encodeURIComponent(path)}`),
  getTree: () => request<TreeEntry[]>("/api/tree"),

  getWreathVerify: () => request<WreathVerification>("/api/wreath/verify"),
  getWreathReport: () => request<WreathReport>("/api/wreath/report"),

  /** Returns null (not an error) when the server has no extraLibraryRoot configured. */
  getExtraLibrary: async (): Promise<ExtraLibraryEntry[] | null> => {
    const response = await fetch("/api/library/extra");
    if (response.status === 404) {
      return null;
    }
    if (!response.ok) {
      throw new WorkbenchApiError("Failed to load the extra library source.");
    }
    return (await response.json()) as ExtraLibraryEntry[];
  },

  getExtraLibraryContent: (path: string) =>
    request<{ path: string; content: string }>(`/api/library/extra/content?path=${encodeURIComponent(path)}`),

  captureIncoming: (input: { title?: string; body: string }) =>
    request<IncomingText>("/api/incoming", { method: "POST", body: JSON.stringify(input) }),

  startProcessingIncoming: (id: string) =>
    request<IncomingText>(`/api/incoming/${encodeURIComponent(id)}/start-processing`, { method: "POST" }),

  archiveIncoming: (id: string) =>
    request<IncomingText>(`/api/incoming/${encodeURIComponent(id)}/archive`, { method: "POST" }),

  createFragment: (input: { incomingTextId: string; body: string; title?: string; conceptIds?: string[] }) =>
    request<Fragment>("/api/fragments", { method: "POST", body: JSON.stringify(input) }),

  archiveFragment: (id: string) =>
    request<Fragment>(`/api/fragments/${encodeURIComponent(id)}/archive`, { method: "POST" }),

  insertFragment: (input: { fragmentId: string; targetChapterPath: string }) =>
    request<Insertion>("/api/insertions", { method: "POST", body: JSON.stringify(input) }),

  bulkInsert: (input: Array<{ fragmentId: string; targetChapterPath: string }>) =>
    request<Insertion[]>("/api/insertions/bulk", { method: "POST", body: JSON.stringify({ insertions: input }) }),

  updateIncomingText: (id: string, input: { title?: string | null; note?: string | null }) =>
    request<IncomingText>(`/api/incoming/${encodeURIComponent(id)}/update`, {
      method: "POST",
      body: JSON.stringify(input),
    }),

  updateFragment: (id: string, input: { title?: string | null; text?: string; note?: string | null; conceptIds?: string[] | null }) =>
    request<Fragment>(`/api/fragments/${encodeURIComponent(id)}/update`, {
      method: "POST",
      body: JSON.stringify(input),
    }),

  updateInsertion: (id: string, input: { targetChapterPath?: string; positionNote?: string | null; note?: string | null }) =>
    request<Insertion>(`/api/insertions/${encodeURIComponent(id)}/update`, {
      method: "POST",
      body: JSON.stringify(input),
    }),

  addConcept: (input: { label: string; note?: string }) =>
    request<Concept>("/api/concepts", { method: "POST", body: JSON.stringify(input) }),

  getConcepts: () => request<ConceptWithCount[]>("/api/concepts"),

  getAnalysisSource: () => request<SourceAnalysis[]>("/api/analysis/source"),

  getOverview: () => request<Overview>("/api/overview"),

  suggestFragment: (text: string) =>
    request<{ ok: boolean; title?: string; concepts: string[] }>("/api/suggestions", {
      method: "POST",
      body: JSON.stringify({ text }),
    }),

  indexFragments: () =>
    request<{ ok: boolean; indexed: number }>("/api/semantic/index-fragments", { method: "POST" }),

  semanticSearch: (query: string, limit = 5) =>
    request<{ ok: boolean; results: Array<{ fragmentId: string; title?: string; text: string; score: number }> }>(
      "/api/semantic/search",
      { method: "POST", body: JSON.stringify({ query, limit }) },
    ),
};

/** Tauri-based API (standalone desktop app, no separate Node server needed). */
export const tauriApi = {
  openFolderPath: async (): Promise<string | null> => {
    const result = await open({ directory: true, multiple: false });
    if (Array.isArray(result)) return result[0] ?? null;
    return result ?? null;
  },
  openBundleFile: async (): Promise<string | null> => {
    const path = await open({ multiple: false, filters: [{ name: "Atmavictu bundle", extensions: ["json"] }] });
    return typeof path === "string" ? path : null;
  },
  saveBundlePath: async (defaultName: string): Promise<string | null> => save({ defaultPath: defaultName, filters: [{ name: "Atmavictu bundle", extensions: ["json"] }] }),
  saveLocalBundle: async (defaultName: string, content: string): Promise<string | null> => {
    const path = await save({ defaultPath: defaultName, filters: [{ name: "Atmavictu bundle", extensions: ["json"] }] });
    if (!path) return null;
    await writeTextFile(path, content);
    return path;
  },
  readLocalBundle: async (path: string): Promise<string> => readTextFile(path),
  exportProjectBackup: (projectRoot: string, destination: string) => invoke<BundlePreview>("export_project_backup", { projectRoot, destination }),
  restoreBackup: (bundlePath: string, destination: string, overwrite: boolean) => invoke<BundlePreview>("restore_backup", { bundlePath, destination, overwrite }),
  previewBackup: (bundlePath: string) => invoke<BundlePreview>("preview_backup", { bundlePath }),
  exportCaseBundle: (projectRoot: string, caseId: string, destination: string) => invoke<BundlePreview>("export_case_bundle", { projectRoot, caseId, destination }),
  previewCaseImport: (bundlePath: string) => invoke<BundlePreview>("preview_case_import", { bundlePath }),
  importCaseBundle: (projectRoot: string, bundlePath: string) => invoke<BundlePreview>("import_case_bundle", { projectRoot, bundlePath }),
  listCases: (projectRoot: string) => invoke<VblCase[]>("list_cases", { projectRoot }),
  createCase: (projectRoot: string, input: { title: string; claim: string; reporter: string }) => invoke<VblCase>("create_case", { projectRoot, ...input }),
  addCaseEvidence: (projectRoot: string, caseId: string, input: { label: string; source: string; content: string; actor: string }) => invoke<VblCase>("add_case_evidence", { projectRoot, caseId, ...input }),
  recordCaseReview: (projectRoot: string, caseId: string, input: { reviewer: string; executor: string; outcome: "SUPPORTED" | "DISPUTED" | "INCONCLUSIVE"; scope: string; findings: string[] }) => invoke<VblCase>("record_case_review", { projectRoot, caseId, ...input }),
  addCaseAction: (projectRoot: string, caseId: string, input: { description: string; owner: string; actor: string }) => invoke<VblCase>("add_case_action", { projectRoot, caseId, ...input }),
  updateCaseAction: (projectRoot: string, caseId: string, actionId: string, status: "OPEN" | "DONE", actor: string) => invoke<VblCase>("update_case_action", { projectRoot, caseId, actionId, status, actor }),
  openFolder: async (): Promise<string | null> => {
    const selected = await open({
      directory: true,
      multiple: false,
    });
    if (Array.isArray(selected)) {
      return selected[0] ?? null;
    }
    return selected ?? null;
  },

  readManifest: async (projectRoot: string): Promise<WorkbenchManifest> => {
    return invoke("read_manifest", { projectRoot });
  },

  verifyManifest: async (projectRoot: string): Promise<ManifestValidationResult> => invoke("verify_manifest", { projectRoot }),

  readSeal: async (projectRoot: string): Promise<ManifestSeal | null> => {
    return invoke("read_seal", { projectRoot });
  },

  verifyWreath: async (projectRoot: string): Promise<WreathVerification> => {
    return invoke("verify_wreath", { projectRoot });
  },

  detectDrift: async (projectRoot: string): Promise<WreathDriftResult> => {
    return invoke("detect_drift", { projectRoot });
  },

  getWreathReport: async (): Promise<WreathReport | null> => null,
};

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
  WorkbenchManifest,
} from "./types";

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
  getManifest: () => request<WorkbenchManifest>("/api/manifest"),
  getVerify: () => request<ManifestValidationResult>("/api/verify"),
  getLibrary: () => request<LibraryEntry[]>("/api/library"),
  getLibraryContent: (path: string) =>
    request<{ path: string; content: string }>(`/api/library/content?path=${encodeURIComponent(path)}`),
  getTree: () => request<TreeEntry[]>("/api/tree"),

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

  createFragment: (input: { incomingTextId: string; body: string }) =>
    request<Fragment>("/api/fragments", { method: "POST", body: JSON.stringify(input) }),

  archiveFragment: (id: string) =>
    request<Fragment>(`/api/fragments/${encodeURIComponent(id)}/archive`, { method: "POST" }),

  insertFragment: (input: { fragmentId: string; targetChapterPath: string }) =>
    request<Insertion>("/api/insertions", { method: "POST", body: JSON.stringify(input) }),

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
};

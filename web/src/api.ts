import type {
  Fragment,
  IncomingText,
  Insertion,
  LibraryEntry,
  ManifestValidationResult,
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
  getTree: () => request<TreeEntry[]>("/api/tree"),

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
};

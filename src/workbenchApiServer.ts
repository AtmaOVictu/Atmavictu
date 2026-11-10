import { createServer, type Server } from "node:http";
import { readdir, readFile } from "node:fs/promises";
import { isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

import express, { type Express, type NextFunction, type Request, type Response } from "express";

import {
  addConcept,
  archiveFragment,
  archiveIncoming,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
  updateFragment,
  updateIncomingText,
  updateInsertion,
  validateManifest,
  type Fragment,
  type IncomingText,
  type Insertion,
  type WorkbenchManifest,
} from "./workbenchManifest.js";
import {
  captureIncomingText,
  ensureManifestFile,
  getManifestPath,
  ManifestRepositoryError,
  writeManifestToFile,
} from "./workbenchManifestRepository.js";

import {
  buildSuggestionPrompt,
  parseSuggestionResponse,
  SUGGESTION_MODEL,
} from "./workbenchSuggestions.js";
import {
  buildEmbeddingRequest,
  buildQdrantCollectionBody,
  buildQdrantSearchBody,
  buildQdrantUpsertBody,
  EMBEDDING_DIMENSIONS,
  parseEmbeddingResponse,
  parseQdrantSearchResponse,
  QDRANT_COLLECTION,
} from "./workbenchSemantic.js";

const IGNORED_ROOT_ENTRIES = new Set(["book.workbench.json", "node_modules", ".git"]);
const DELO_ARTIFACT_MARKER = "<!-- delo-artifact:v1";
const DELO_ARTIFACT_MARKER_END = "-->";
const DEFAULT_OLLAMA_URL = "http://localhost:11434";
const DEFAULT_QDRANT_URL = "http://localhost:6333";

export interface WorkbenchApiOptions {
  /**
   * Optional second, read-only source root browsable alongside Knjiznica's
   * own projectRoot — e.g. a Smisel WorkShade `drafts/` folder. Generic by
   * design: Atmavictu itself has no concept of "Delo" or "WorkShade," this
   * is just an arbitrary extra folder a caller may point at anything.
   */
  extraLibraryRoot?: string;
  /**
   * Base URL of an Ollama instance used for the optional LLM-assisted
   * fragment title/concept suggestions. Defaults to the local Ollama. When
   * unreachable, the suggestions endpoint degrades gracefully (never blocks
   * the workbench).
   */
  ollamaUrl?: string;
  /**
   * Base URL of a Qdrant instance used for optional semantic search over
   * fragments. Defaults to the local Qdrant. When unreachable, the semantic
   * endpoints degrade gracefully.
   */
  qdrantUrl?: string;
}

/**
 * Per-project-root write locks for manifest read-modify-write cycles.
 * Without serialization, two concurrent mutations can interleave
 * (read A, read B, write A, write B) and one update is silently lost.
 * One lock entry per distinct root lives for the process lifetime — a
 * server holds a small, fixed set of roots, so the map cannot grow unbounded.
 */
const manifestWriteLocks = new Map<string, Promise<void>>();

/**
 * Serializes manifest mutations per project root. A failed operation never
 * poisons the queue: the next operation starts regardless of the previous
 * outcome, while callers still receive their own result or rejection.
 */
export function withManifestLock<T>(projectRoot: string, operation: () => Promise<T>): Promise<T> {
  const lockKey = resolve(requireNonEmptyString("projectRoot", projectRoot));
  const previousLock = manifestWriteLocks.get(lockKey) ?? Promise.resolve();
  const release = previousLock.then(
    () => undefined,
    () => undefined,
  );
  const result = release.then(operation);
  manifestWriteLocks.set(
    lockKey,
    result.then(
      () => undefined,
      () => undefined,
    ),
  );
  return result;
}

/**
 * Deterministic Qdrant point id per fragment, derived from the fragment id.
 * Re-indexing upserts onto the same point instead of accumulating duplicate
 * vectors for one fragment (randomUUID() created a fresh point every run).
 */
export function fragmentPointId(fragmentId: string): string {
  const digest = createHash("sha256")
    .update(`workbench-fragment:${fragmentId}`)
    .digest("hex")
    .slice(0, 32);
  return [
    digest.slice(0, 8),
    digest.slice(8, 12),
    digest.slice(12, 16),
    digest.slice(16, 20),
    digest.slice(20, 32),
  ].join("-");
}

export function createWorkbenchApiApp(projectRoot: string, options: WorkbenchApiOptions = {}): Express {
  const normalizedProjectRoot = requireNonEmptyString("projectRoot", projectRoot);
  const extraLibraryRoot = options.extraLibraryRoot?.trim() || undefined;
  const ollamaUrl = options.ollamaUrl?.trim() || DEFAULT_OLLAMA_URL;
  const qdrantUrl = options.qdrantUrl?.trim() || DEFAULT_QDRANT_URL;
  const app = express();
  app.use(express.json());

  app.get("/api/manifest", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    res.json(manifest);
  }));

  app.get("/api/verify", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    res.json(validateManifest(manifest));
  }));

  app.get("/api/library", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const capturedSourcePaths = new Set(manifest.incomingTexts.map((incomingText) => incomingText.sourcePath));
    const files = await listProjectFiles(normalizedProjectRoot);
    res.json(
      files.map((filePath) => ({
        path: filePath,
        captured: capturedSourcePaths.has(filePath),
      })),
    );
  }));

  app.get("/api/library/content", asyncRoute(async (req, res) => {
    const filePath = requireQueryString(req, "path");
    const resolvedPath = resolveWithinRoot(normalizedProjectRoot, filePath, "path");
    try {
      res.json({ path: filePath, content: await readFile(resolvedPath, "utf8") });
    } catch (error) {
      if (isNodeErrnoException(error) && error.code === "ENOENT") {
        res.status(404).json({ error: `File not found in library: ${filePath}` });
        return;
      }
      throw error;
    }
  }));

  app.get("/api/library/extra", asyncRoute(async (_req, res) => {
    if (extraLibraryRoot === undefined) {
      res.status(404).json({ error: "No extraLibraryRoot configured for this server." });
      return;
    }
    const files = await listProjectFiles(extraLibraryRoot);
    const entries = await Promise.all(
      files.map(async (filePath) => {
        try {
          const content = await readFile(join(extraLibraryRoot, filePath), "utf8");
          return { path: filePath, deloProvenance: parseDeloProvenance(content) };
        } catch (error) {
          // Name the failure per file instead of failing the whole listing.
          return { path: filePath, deloProvenance: null, readError: errorMessage(error) };
        }
      }),
    );
    res.json(entries);
  }));

  app.get("/api/library/extra/content", asyncRoute(async (req, res) => {
    if (extraLibraryRoot === undefined) {
      res.status(404).json({ error: "No extraLibraryRoot configured for this server." });
      return;
    }
    const filePath = requireQueryString(req, "path");
    const resolvedPath = resolveWithinRoot(extraLibraryRoot, filePath, "path");
    try {
      res.json({ path: filePath, content: await readFile(resolvedPath, "utf8") });
    } catch (error) {
      if (isNodeErrnoException(error) && error.code === "ENOENT") {
        res.status(404).json({ error: `File not found in extra library: ${filePath}` });
        return;
      }
      throw error;
    }
  }));

  app.get("/api/tree", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const insertionsByPath = new Map<string, number>();
    for (const insertion of manifest.insertions) {
      insertionsByPath.set(
        insertion.targetChapterPath,
        (insertionsByPath.get(insertion.targetChapterPath) ?? 0) + 1,
      );
    }
    const files = await listProjectFiles(normalizedProjectRoot);
    res.json(
      files.map((filePath) => ({
        path: filePath,
        insertionCount: insertionsByPath.get(filePath) ?? 0,
      })),
    );
  }));

  app.post("/api/incoming", asyncRoute(async (req, res) => {
    const { title, body, note, sourcePath } = req.body as Record<string, unknown>;
    const result = await withManifestLock(normalizedProjectRoot, () =>
      captureIncomingText(normalizedProjectRoot, {
        body: requireBodyString("body", body),
        ...(typeof title === "string" ? { title } : {}),
        ...(typeof note === "string" ? { note } : {}),
        ...(typeof sourcePath === "string" ? { sourcePath } : {}),
      }),
    );
    res.status(201).json(result.value);
  }));

  app.post(
    "/api/incoming/:id/start-processing",
    mutateRoute(normalizedProjectRoot, (manifest, req) =>
      startProcessingIncoming(manifest, req.params.id!),
    ),
  );

  app.post(
    "/api/incoming/:id/archive",
    mutateRoute(normalizedProjectRoot, (manifest, req) => archiveIncoming(manifest, req.params.id!)),
  );

  app.post(
    "/api/fragments",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { incomingTextId, body, title, conceptIds } = req.body as Record<string, unknown>;
      const nextConceptIds = readOptionalStringArray("conceptIds", conceptIds);
      return createFragmentFromIncoming(
        manifest,
        requireBodyString("incomingTextId", incomingTextId),
        requireBodyString("body", body),
        {
          ...(typeof title === "string" ? { title } : {}),
          ...(nextConceptIds !== undefined ? { conceptIds: nextConceptIds } : {}),
        },
      );
    }, 201),
  );

  app.post(
    "/api/fragments/:id/archive",
    mutateRoute(normalizedProjectRoot, (manifest, req) => archiveFragment(manifest, req.params.id!)),
  );

  app.post(
    "/api/insertions",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { fragmentId, targetChapterPath } = req.body as Record<string, unknown>;
      return insertFragmentIntoChapter(
        manifest,
        requireBodyString("fragmentId", fragmentId),
        requireBodyString("targetChapterPath", targetChapterPath),
      );
    }, 201),
  );

  app.post(
    "/api/incoming/:id/update",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { title, note } = req.body as Record<string, unknown>;
      const nextTitle = readOptionalNullableString("title", title);
      const nextNote = readOptionalNullableString("note", note);
      return updateIncomingText(manifest, req.params.id!, {
        ...(nextTitle !== undefined ? { title: nextTitle } : {}),
        ...(nextNote !== undefined ? { note: nextNote } : {}),
      });
    }),
  );

  app.post(
    "/api/fragments/:id/update",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { title, text, note, conceptIds } = req.body as Record<string, unknown>;
      const nextTitle = readOptionalNullableString("title", title);
      const nextText = readOptionalNonEmptyString("text", text);
      const nextNote = readOptionalNullableString("note", note);
      const nextConceptIds = readOptionalNullableStringArray("conceptIds", conceptIds);
      return updateFragment(manifest, req.params.id!, {
        ...(nextTitle !== undefined ? { title: nextTitle } : {}),
        ...(nextText !== undefined ? { text: nextText } : {}),
        ...(nextNote !== undefined ? { note: nextNote } : {}),
        ...(nextConceptIds !== undefined ? { conceptIds: nextConceptIds } : {}),
      });
    }),
  );

  app.post(
    "/api/insertions/:id/update",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { targetChapterPath, positionNote, note } = req.body as Record<string, unknown>;
      const nextTargetChapterPath = readOptionalNonEmptyString("targetChapterPath", targetChapterPath);
      const nextPositionNote = readOptionalNullableString("positionNote", positionNote);
      const nextNote = readOptionalNullableString("note", note);
      return updateInsertion(manifest, req.params.id!, {
        ...(nextTargetChapterPath !== undefined ? { targetChapterPath: nextTargetChapterPath } : {}),
        ...(nextPositionNote !== undefined ? { positionNote: nextPositionNote } : {}),
        ...(nextNote !== undefined ? { note: nextNote } : {}),
      });
    }),
  );

  app.post(
    "/api/concepts",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { label, note } = req.body as Record<string, unknown>;
      return addConcept(manifest, {
        label: requireBodyString("label", label),
        ...(typeof note === "string" ? { note } : {}),
      });
    }, 201),
  );

  app.get("/api/concepts", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const concepts = manifest.concepts ?? [];
    const fragmentCounts = new Map<string, number>();
    for (const fragment of manifest.fragments) {
      for (const conceptId of fragment.conceptIds ?? []) {
        fragmentCounts.set(conceptId, (fragmentCounts.get(conceptId) ?? 0) + 1);
      }
    }
    res.json(
      concepts.map((concept) => ({
        id: concept.id,
        label: concept.label,
        note: concept.note,
        fragmentCount: fragmentCounts.get(concept.id) ?? 0,
      })),
    );
  }));

  app.get("/api/analysis/source", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const fragmentsByIncoming = new Map<string, Fragment[]>();
    for (const fragment of manifest.fragments) {
      const list = fragmentsByIncoming.get(fragment.incomingTextId) ?? [];
      list.push(fragment);
      fragmentsByIncoming.set(fragment.incomingTextId, list);
    }
    res.json(
      manifest.incomingTexts.map((incoming) => {
        const fragments = fragmentsByIncoming.get(incoming.id) ?? [];
        return {
          id: incoming.id,
          title: incoming.title,
          sourcePath: incoming.sourcePath,
          status: incoming.status,
          fragmentCount: fragments.length,
          draftCount: fragments.filter((f) => f.status === "draft").length,
          insertedCount: fragments.filter((f) => f.status === "inserted").length,
          archivedCount: fragments.filter((f) => f.status === "archived").length,
        };
      }),
    );
  }));

  app.get("/api/overview", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const byChapter = new Map<string, number>();
    for (const insertion of manifest.insertions) {
      byChapter.set(insertion.targetChapterPath, (byChapter.get(insertion.targetChapterPath) ?? 0) + 1);
    }
    res.json({
      manifestVersion: manifest.manifestVersion,
      incomingTotal: manifest.incomingTexts.length,
      fragmentTotal: manifest.fragments.length,
      insertionTotal: manifest.insertions.length,
      conceptTotal: manifest.concepts?.length ?? 0,
      chapters: Array.from(byChapter.entries()).map(([path, count]) => ({ path, count })),
    });
  }));

  app.post("/api/suggestions", asyncRoute(async (req, res) => {
    const text = (req.body as Record<string, unknown> | undefined)?.text;
    if (typeof text !== "string" || text.trim().length === 0) {
      res.status(400).json({ ok: false, error: "text is a required non-empty string." });
      return;
    }
    try {
      const suggestions = await requestOllamaSuggestions(ollamaUrl, text);
      res.json({ ok: true, ...suggestions });
    } catch (error) {
      // Degrade gracefully: never block the workbench on an unreachable model,
      // but never swallow the cause either — name it in the response.
      res.status(502).json({
        ok: false,
        error: "suggestion service is unavailable.",
        cause: errorMessage(error),
      });
    }
  }));

  app.post("/api/semantic/index-fragments", asyncRoute(async (_req, res) => {
    const manifest = await ensureManifestFile(normalizedProjectRoot);
    const fragments = manifest.fragments;
    if (fragments.length === 0) {
      res.json({ ok: true, indexed: 0 });
      return;
    }
    try {
      const points: Array<{ id: string; vector: number[]; payload: Record<string, unknown> }> = [];
      for (const fragment of fragments) {
        const vector = await embedText(ollamaUrl, fragment.text);
        if (vector.length === 0) {
          continue;
        }
        points.push({
          id: fragmentPointId(fragment.id),
          vector,
          payload: {
            fragmentId: fragment.id,
            title: fragment.title,
            text: fragment.text,
          },
        });
      }
      await ensureQdrantCollection(qdrantUrl);
      if (points.length > 0) {
        await qdrantSend(qdrantUrl, `/collections/${QDRANT_COLLECTION}/points?wait=true`, "PUT", buildQdrantUpsertBody(points));
      }
      res.json({ ok: true, indexed: points.length });
    } catch (error) {
      res.status(502).json({
        ok: false,
        error: "semantic index service is unavailable.",
        cause: errorMessage(error),
      });
    }
  }));

  app.post("/api/semantic/search", asyncRoute(async (req, res) => {
    const body = (req.body as Record<string, unknown> | undefined) ?? {};
    const query = body.query;
    const limit = typeof body.limit === "number" ? Math.min(Math.max(Math.floor(body.limit), 1), 20) : 5;
    if (typeof query !== "string" || query.trim().length === 0) {
      res.status(400).json({ ok: false, error: "query is a required non-empty string." });
      return;
    }
    try {
      const vector = await embedText(ollamaUrl, query);
      if (vector.length === 0) {
        res.status(502).json({
          ok: false,
          error: "could not embed the query.",
          cause: "embedding service returned an empty vector.",
        });
        return;
      }
      const data = await qdrantSend(qdrantUrl, `/collections/${QDRANT_COLLECTION}/points/search`, "POST", buildQdrantSearchBody(vector, limit));
      res.json({ ok: true, results: parseQdrantSearchResponse(data) });
    } catch (error) {
      res.status(502).json({
        ok: false,
        error: "semantic search service is unavailable.",
        cause: errorMessage(error),
      });
    }
  }));

  app.use(errorHandler);

  return app;
}

export function startWorkbenchApiServer(
  projectRoot: string,
  port: number,
  options?: WorkbenchApiOptions,
): Server {
  const app = createWorkbenchApiApp(projectRoot, options);
  return createServer(app).listen(port);
}

/**
 * Shared read-modify-write wrapper for the 5 pure model operations
 * (startProcessingIncoming/createFragmentFromIncoming/insertFragmentIntoChapter/
 * archiveIncoming/archiveFragment): none of them persist on their own, so every
 * route needs the same read -> apply -> write sequence. The whole cycle runs
 * under the per-root manifest lock so concurrent requests cannot interleave.
 */
function mutateRoute<TValue>(
  projectRoot: string,
  apply: (manifest: WorkbenchManifest, req: Request) => { manifest: WorkbenchManifest; value: TValue },
  successStatus = 200,
) {
  return asyncRoute(async (req, res) => {
    await withManifestLock(projectRoot, async () => {
      const manifestPath = getManifestPath(projectRoot);
      const manifest = await ensureManifestFile(projectRoot);
      const result = apply(manifest, req);
      await writeManifestToFile(manifestPath, result.manifest);
      res.status(successStatus).json(result.value);
    });
  });
}

function asyncRoute(handler: (req: Request, res: Response) => Promise<void>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    handler(req, res).catch(next);
  };
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function errorHandler(error: unknown, _req: Request, res: Response, _next: NextFunction): void {
  const message = errorMessage(error);
  if (error instanceof ManifestRepositoryError) {
    // The manifest storage itself is broken — this is never the client's fault.
    res.status(500).json({ error: message, code: error.code });
    return;
  }
  res.status(400).json({ error: message });
}

async function listProjectFiles(projectRoot: string): Promise<string[]> {
  const results: string[] = [];

  async function walk(currentDirectory: string): Promise<void> {
    const entries = await readdir(join(projectRoot, currentDirectory), { withFileTypes: true });
    for (const entry of entries) {
      if (IGNORED_ROOT_ENTRIES.has(entry.name)) {
        continue;
      }
      const entryRelativePath = currentDirectory === "." ? entry.name : `${currentDirectory}/${entry.name}`;
      if (entry.isDirectory()) {
        await walk(entryRelativePath);
      } else if (entry.isFile()) {
        results.push(entryRelativePath.split("\\").join("/"));
      }
    }
  }

  await walk(".");
  return results.sort();
}

async function embedText(ollamaUrl: string, text: string): Promise<number[]> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${ollamaUrl.replace(/\/$/, "")}/api/embed`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(buildEmbeddingRequest(text)),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`Ollama embed responded ${response.status}`);
    }
    const data = (await response.json()) as unknown;
    return parseEmbeddingResponse(data);
  } finally {
    clearTimeout(timeout);
  }
}

async function ensureQdrantCollection(qdrantUrl: string): Promise<void> {
  // 200 = created, 409 = already exists (both fine).
  await qdrantSend(
    qdrantUrl,
    `/collections/${QDRANT_COLLECTION}`,
    "PUT",
    buildQdrantCollectionBody(EMBEDDING_DIMENSIONS),
    new Set([200, 409]),
  );
}

async function qdrantSend(
  qdrantUrl: string,
  path: string,
  method: "POST" | "PUT",
  body: unknown,
  accepted: Set<number> = new Set([200]),
): Promise<unknown> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${qdrantUrl.replace(/\/$/, "")}${path}`, {
      method,
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    if (!accepted.has(response.status)) {
      throw new Error(`Qdrant ${path} responded ${response.status}`);
    }
    return (await response.json()) as unknown;
  } finally {
    clearTimeout(timeout);
  }
}

async function requestOllamaSuggestions(
  ollamaUrl: string,
  text: string,
): Promise<{ title?: string; concepts: string[] }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${ollamaUrl.replace(/\/$/, "")}/api/generate`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        model: SUGGESTION_MODEL,
        prompt: buildSuggestionPrompt(text),
        stream: false,
        options: { temperature: 0.3 },
      }),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`Ollama responded ${response.status}`);
    }
    const data = (await response.json()) as { response?: string };
    return parseSuggestionResponse(data.response ?? "");
  } finally {
    clearTimeout(timeout);
  }
}

function requireBodyString(name: string, value: unknown): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${name} must be a non-empty string.`);
  }
  return value;
}

function requireQueryString(req: Request, name: string): string {
  const value = req.query[name];
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`Query parameter ${name} must be a non-empty string.`);
  }
  return value;
}

/**
 * undefined = field absent from the request (leave untouched);
 * null = explicit removal; otherwise a non-empty string. Anything else is a
 * named 400 instead of a silent `as string | null` cast that crashes later
 * deep inside the model layer.
 */
function readOptionalNullableString(name: string, value: unknown): string | null | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (value === null) {
    return null;
  }
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${name} must be a non-empty string or null.`);
  }
  return value;
}

/** undefined = absent; otherwise a non-empty string (no null removal channel). */
function readOptionalNonEmptyString(name: string, value: unknown): string | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${name} must be a non-empty string.`);
  }
  return value;
}

/** undefined = absent; otherwise a non-empty-string array (silently ignoring a wrong type hides client bugs). */
function readOptionalStringArray(name: string, value: unknown): string[] | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (!Array.isArray(value) || !value.every((item) => typeof item === "string" && item.trim().length > 0)) {
    throw new Error(`${name} must be an array of non-empty strings.`);
  }
  return value;
}

/** undefined = absent; null = removal; otherwise a non-empty-string array. */
function readOptionalNullableStringArray(name: string, value: unknown): string[] | null | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (value === null) {
    return null;
  }
  if (!Array.isArray(value) || !value.every((item) => typeof item === "string" && item.trim().length > 0)) {
    throw new Error(`${name} must be an array of non-empty strings or null.`);
  }
  return value;
}

/** Same escape-guard shape as workbenchManifestRepository's resolveProjectFilePath. */
function resolveWithinRoot(root: string, relativeFilePath: string, name: string): string {
  const normalizedRoot = resolve(root);

  if (isAbsolute(relativeFilePath)) {
    throw new Error(`${name} must be a relative path: ${relativeFilePath}`);
  }

  const resolvedPath = resolve(normalizedRoot, relativeFilePath);
  const relativeToRoot = relative(normalizedRoot, resolvedPath);

  if (relativeToRoot.startsWith("..") || isAbsolute(relativeToRoot)) {
    throw new Error(`${name} must stay within its root: ${relativeFilePath}`);
  }

  return resolvedPath;
}

export interface DeloArtifactProvenance {
  artifactId: string;
  outputType: string;
  nextAction?: string;
  createdAt?: string;
}

/**
 * Best-effort parse of the delo-artifact:v1 envelope canvas_server.py writes
 * (see Projects/WorkShade/scripts/canvas_server.py's `_delo_render_artifact_v1`).
 * Not every file under an extraLibraryRoot carries this — most of WorkShade's
 * own `drafts/` folder is /dialektika and /seciraj output with no envelope at
 * all, so a null return here is the common case, not an error.
 */
function parseDeloProvenance(content: string): DeloArtifactProvenance | null {
  if (!content.startsWith(DELO_ARTIFACT_MARKER)) {
    return null;
  }
  const end = content.indexOf(DELO_ARTIFACT_MARKER_END);
  if (end === -1) {
    return null;
  }
  const envelopeRaw = content.slice(DELO_ARTIFACT_MARKER.length, end).trim();

  try {
    const envelope = JSON.parse(envelopeRaw) as Record<string, unknown>;
    if (typeof envelope.artifact_id !== "string" || typeof envelope.output_type !== "string") {
      return null;
    }
    return {
      artifactId: envelope.artifact_id,
      outputType: envelope.output_type,
      ...(typeof envelope.next_action === "string" ? { nextAction: envelope.next_action } : {}),
      ...(typeof envelope.created_at === "string" ? { createdAt: envelope.created_at } : {}),
    };
  } catch {
    return null;
  }
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function isNodeErrnoException(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error && typeof (error as NodeJS.ErrnoException).code === "string";
}

function requireNonEmptyString(name: string, value: string): string {
  if (value.trim().length === 0) {
    throw new Error(`${name} must be a non-empty string.`);
  }
  return value;
}

function isDirectExecution(): boolean {
  const entryPath = process.argv[1];
  if (entryPath === undefined) {
    return false;
  }
  return resolve(entryPath) === fileURLToPath(import.meta.url);
}

if (isDirectExecution()) {
  const projectRoot = process.argv[2];
  const port = Number(process.argv[3] ?? "4173");
  const extraLibraryRoot = process.argv[4];

  if (projectRoot === undefined || projectRoot.trim().length === 0) {
    process.stderr.write(
      "Usage: node build/src/workbenchApiServer.js <projectRoot> [port] [extraLibraryRoot]\n",
    );
    process.exitCode = 1;
  } else if (!Number.isInteger(port) || port < 1 || port > 65535) {
    process.stderr.write(
      `Port must be an integer between 1 and 65535, received: ${process.argv[3] ?? ""}\n`,
    );
    process.exitCode = 1;
  } else {
    startWorkbenchApiServer(
      projectRoot,
      port,
      extraLibraryRoot !== undefined ? { extraLibraryRoot } : {},
    );
    process.stdout.write(`Atmavictu workbench API listening on http://localhost:${port}\n`);
    if (extraLibraryRoot !== undefined) {
      process.stdout.write(`Extra library root: ${extraLibraryRoot}\n`);
    }
  }
}

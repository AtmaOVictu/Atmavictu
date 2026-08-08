import { createServer, type Server } from "node:http";
import { readdir, readFile } from "node:fs/promises";
import { isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import express, { type Express, type NextFunction, type Request, type Response } from "express";

import {
  archiveFragment,
  archiveIncoming,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
  updateFragment,
  updateIncomingText,
  updateInsertion,
  validateManifest,
  type WorkbenchManifest,
} from "./workbenchManifest.js";
import {
  captureIncomingText,
  ensureManifestFile,
  getManifestPath,
  writeManifestToFile,
} from "./workbenchManifestRepository.js";

const IGNORED_ROOT_ENTRIES = new Set(["book.workbench.json", "node_modules", ".git"]);
const DELO_ARTIFACT_MARKER = "<!-- delo-artifact:v1";
const DELO_ARTIFACT_MARKER_END = "-->";

export interface WorkbenchApiOptions {
  /**
   * Optional second, read-only source root browsable alongside Knjiznica's
   * own projectRoot — e.g. a Smisel WorkShade `drafts/` folder. Generic by
   * design: Atmavictu itself has no concept of "Delo" or "WorkShade," this
   * is just an arbitrary extra folder a caller may point at anything.
   */
  extraLibraryRoot?: string;
}

export function createWorkbenchApiApp(projectRoot: string, options: WorkbenchApiOptions = {}): Express {
  const normalizedProjectRoot = requireNonEmptyString("projectRoot", projectRoot);
  const extraLibraryRoot = options.extraLibraryRoot?.trim() || undefined;
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
    res.json({ path: filePath, content: await readFile(resolvedPath, "utf8") });
  }));

  app.get("/api/library/extra", asyncRoute(async (_req, res) => {
    if (extraLibraryRoot === undefined) {
      res.status(404).json({ error: "No extraLibraryRoot configured for this server." });
      return;
    }
    const files = await listProjectFiles(extraLibraryRoot);
    const entries = await Promise.all(
      files.map(async (filePath) => {
        const content = await readFile(join(extraLibraryRoot, filePath), "utf8");
        return { path: filePath, deloProvenance: parseDeloProvenance(content) };
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
    res.json({ path: filePath, content: await readFile(resolvedPath, "utf8") });
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
    const result = await captureIncomingText(normalizedProjectRoot, {
      body: requireBodyString("body", body),
      ...(typeof title === "string" ? { title } : {}),
      ...(typeof note === "string" ? { note } : {}),
      ...(typeof sourcePath === "string" ? { sourcePath } : {}),
    });
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
      const { incomingTextId, body } = req.body as Record<string, unknown>;
      return createFragmentFromIncoming(
        manifest,
        requireBodyString("incomingTextId", incomingTextId),
        requireBodyString("body", body),
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
      return updateIncomingText(manifest, req.params.id!, {
        ...(title !== undefined ? { title: title as string | null } : {}),
        ...(note !== undefined ? { note: note as string | null } : {}),
      });
    }),
  );

  app.post(
    "/api/fragments/:id/update",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { title, text, note } = req.body as Record<string, unknown>;
      return updateFragment(manifest, req.params.id!, {
        ...(title !== undefined ? { title: title as string | null } : {}),
        ...(text !== undefined ? { text: text as string } : {}),
        ...(note !== undefined ? { note: note as string | null } : {}),
      });
    }),
  );

  app.post(
    "/api/insertions/:id/update",
    mutateRoute(normalizedProjectRoot, (manifest, req) => {
      const { targetChapterPath, positionNote, note } = req.body as Record<string, unknown>;
      return updateInsertion(manifest, req.params.id!, {
        ...(targetChapterPath !== undefined ? { targetChapterPath: targetChapterPath as string } : {}),
        ...(positionNote !== undefined ? { positionNote: positionNote as string | null } : {}),
        ...(note !== undefined ? { note: note as string | null } : {}),
      });
    }),
  );

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
 * route needs the same read -> apply -> write sequence.
 */
function mutateRoute<TValue>(
  projectRoot: string,
  apply: (manifest: WorkbenchManifest, req: Request) => { manifest: WorkbenchManifest; value: TValue },
  successStatus = 200,
) {
  return asyncRoute(async (req, res) => {
    const manifestPath = getManifestPath(projectRoot);
    const manifest = await ensureManifestFile(projectRoot);
    const result = apply(manifest, req);
    await writeManifestToFile(manifestPath, result.manifest);
    res.status(successStatus).json(result.value);
  });
}

function asyncRoute(handler: (req: Request, res: Response) => Promise<void>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    handler(req, res).catch(next);
  };
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function errorHandler(error: unknown, _req: Request, res: Response, _next: NextFunction): void {
  const message = error instanceof Error ? error.message : String(error);
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

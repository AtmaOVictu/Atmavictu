import { createServer, type Server } from "node:http";
import { readdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import express, { type Express, type NextFunction, type Request, type Response } from "express";

import {
  archiveFragment,
  archiveIncoming,
  createFragmentFromIncoming,
  insertFragmentIntoChapter,
  startProcessingIncoming,
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

export function createWorkbenchApiApp(projectRoot: string): Express {
  const normalizedProjectRoot = requireNonEmptyString("projectRoot", projectRoot);
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

  app.use(errorHandler);

  return app;
}

export function startWorkbenchApiServer(projectRoot: string, port: number): Server {
  const app = createWorkbenchApiApp(projectRoot);
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

  if (projectRoot === undefined || projectRoot.trim().length === 0) {
    process.stderr.write("Usage: node build/src/workbenchApiServer.js <projectRoot> [port]\n");
    process.exitCode = 1;
  } else {
    startWorkbenchApiServer(projectRoot, port);
    process.stdout.write(`Atmavictu workbench API listening on http://localhost:${port}\n`);
  }
}

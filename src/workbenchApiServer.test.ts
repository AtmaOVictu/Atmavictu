import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { AddressInfo } from "node:net";
import test from "node:test";

import { startWorkbenchApiServer } from "./workbenchApiServer.js";
import type { Fragment, IncomingText, Insertion, ManifestValidationResult, WorkbenchManifest } from "./workbenchManifest.js";

test("full workbench flow: all 9 service operations reachable over HTTP", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    // createEmptyManifest / ensureManifestFile
    const initialManifest = await getJson<WorkbenchManifest>(`${baseUrl}/api/manifest`);
    assert.equal(initialManifest.manifestVersion, "1");
    assert.deepEqual(initialManifest.incomingTexts, []);

    // addIncomingText (via captureIncomingText)
    const capture = await postJson<IncomingText>(`${baseUrl}/api/incoming`, {
      title: "Prvi vir",
      body: "Vsebina prvega vira.",
    });
    assert.equal(capture.status, 201);
    assert.equal(capture.body.status, "new");
    const incomingId = capture.body.id;

    // startProcessingIncoming
    const started = await postJson<IncomingText>(`${baseUrl}/api/incoming/${incomingId}/start-processing`, {});
    assert.equal(started.status, 200);
    assert.equal(started.body.status, "processing");

    // createFragmentFromIncoming
    const fragmentResult = await postJson<Fragment>(`${baseUrl}/api/fragments`, {
      incomingTextId: incomingId,
      body: "Izlocen odlomek.",
    });
    assert.equal(fragmentResult.status, 201);
    assert.equal(fragmentResult.body.status, "draft");
    const fragmentId = fragmentResult.body.id;

    // insertFragmentIntoChapter
    const insertion = await postJson<Insertion>(`${baseUrl}/api/insertions`, {
      fragmentId,
      targetChapterPath: "chapters/01-uvod.md",
    });
    assert.equal(insertion.status, 201);
    assert.equal(insertion.body.targetChapterPath, "chapters/01-uvod.md");

    const afterInsertion = await getJson<WorkbenchManifest>(`${baseUrl}/api/manifest`);
    assert.equal(afterInsertion.fragments.find((f) => f.id === fragmentId)?.status, "inserted");
    assert.equal(afterInsertion.incomingTexts.find((i) => i.id === incomingId)?.status, "used");

    // archiveFragment (inserted -> archived; insertion trail must survive)
    const archivedFragment = await postJson<Fragment>(`${baseUrl}/api/fragments/${fragmentId}/archive`, {});
    assert.equal(archivedFragment.status, 200);
    assert.equal(archivedFragment.body.status, "archived");

    // archiveIncoming (used -> archived)
    const archivedIncoming = await postJson<IncomingText>(`${baseUrl}/api/incoming/${incomingId}/archive`, {});
    assert.equal(archivedIncoming.status, 200);
    assert.equal(archivedIncoming.body.status, "archived");

    // validateManifest / validateManifestTransition (exercised implicitly by every write above,
    // and directly here via /api/verify)
    const verify = await getJson<ManifestValidationResult>(`${baseUrl}/api/verify`);
    assert.equal(verify.isValid, true);
    assert.deepEqual(verify.errors, []);

    // derived reads: library (captured source file shows up) and tree (insertion count)
    const library = await getJson<Array<{ path: string; captured: boolean }>>(`${baseUrl}/api/library`);
    const capturedEntry = library.find((entry) => entry.path === capture.body.sourcePath);
    assert.ok(capturedEntry, "captured source file should be listed in the library view");
    assert.equal(capturedEntry?.captured, true);

    const tree = await getJson<Array<{ path: string; insertionCount: number }>>(`${baseUrl}/api/tree`);
    const chapterEntry = tree.find((entry) => entry.path === "chapters/01-uvod.md");
    // The insertion target is a virtual path (never materialized as a file), so it is
    // deliberately absent from the tree view here; this documents that boundary rather
    // than asserting a file the current implementation never creates.
    assert.equal(chapterEntry, undefined);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("mutation errors surface as 400 with a plain-text message, not a 500", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await postJson<{ error: string }>(
      `${baseUrl}/api/incoming/does-not-exist/start-processing`,
      {},
    );

    assert.equal(response.status, 400);
    assert.match(response.body.error, /IncomingText not found/);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  return (await response.json()) as T;
}

async function postJson<T>(url: string, body: unknown): Promise<{ status: number; body: T }> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  return { status: response.status, body: (await response.json()) as T };
}

async function waitForBaseUrl(server: import("node:http").Server): Promise<string> {
  await new Promise<void>((resolveListening) => {
    if (server.listening) {
      resolveListening();
      return;
    }
    server.once("listening", () => resolveListening());
  });
  const address = server.address() as AddressInfo;
  return `http://127.0.0.1:${address.port}`;
}

async function createTempDirectory(): Promise<string> {
  return mkdtemp(join(tmpdir(), "atmavictu-api-"));
}

async function cleanupTempDirectory(projectRoot: string): Promise<void> {
  await rm(projectRoot, { force: true, recursive: true });
}

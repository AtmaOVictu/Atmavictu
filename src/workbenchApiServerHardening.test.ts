import assert from "node:assert/strict";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { AddressInfo } from "node:net";
import test from "node:test";

import { fragmentPointId, startWorkbenchApiServer, withManifestLock } from "./workbenchApiServer.js";

test("update routes reject wrong-typed fields with a named 400 instead of a cast crash", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const capture = await postJson<{ id: string }>(`${baseUrl}/api/incoming`, {
      title: "Vir",
      body: "Vsebina vira.",
    });
    const incomingId = capture.body.id;
    await postJson(`${baseUrl}/api/incoming/${incomingId}/start-processing`, {});
    const fragment = await postJson<{ id: string }>(`${baseUrl}/api/fragments`, {
      incomingTextId: incomingId,
      body: "Odlomek.",
    });
    const fragmentId = fragment.body.id;

    const badTitle = await postJson<{ error: string }>(`${baseUrl}/api/incoming/${incomingId}/update`, {
      title: 123,
    });
    assert.equal(badTitle.status, 400);
    assert.match(badTitle.body.error, /title must be a non-empty string or null/);

    const badText = await postJson<{ error: string }>(`${baseUrl}/api/fragments/${fragmentId}/update`, {
      text: 123,
    });
    assert.equal(badText.status, 400);
    assert.match(badText.body.error, /text must be a non-empty string/);

    const badConceptIds = await postJson<{ error: string }>(`${baseUrl}/api/fragments/${fragmentId}/update`, {
      conceptIds: "concept-0001",
    });
    assert.equal(badConceptIds.status, 400);
    assert.match(badConceptIds.body.error, /conceptIds must be an array of non-empty strings or null/);

    const badCreateConceptIds = await postJson<{ error: string }>(`${baseUrl}/api/fragments`, {
      incomingTextId: incomingId,
      body: "Drug odlomek.",
      conceptIds: "concept-0001",
    });
    assert.equal(badCreateConceptIds.status, 400);
    assert.match(badCreateConceptIds.body.error, /conceptIds must be an array of non-empty strings/);

    // The manifest itself must remain valid after every refused write.
    const verify = await getJson<{ isValid: boolean }>(`${baseUrl}/api/verify`);
    assert.equal(verify.isValid, true);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("corrupt manifest storage is a named 500 with the repository code, never a client 400", async () => {
  const projectRoot = await createTempDirectory();
  await writeFile(join(projectRoot, "book.workbench.json"), "{ not json", "utf8");
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await fetch(`${baseUrl}/api/manifest`);
    assert.equal(response.status, 500);
    const body = (await response.json()) as { error: string; code: string };
    assert.equal(body.code, "INVALID_JSON");
    assert.match(body.error, /invalid JSON/);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("structurally invalid manifest on disk is reported as INVALID_MANIFEST 500", async () => {
  const projectRoot = await createTempDirectory();
  await writeFile(
    join(projectRoot, "book.workbench.json"),
    JSON.stringify({ manifestVersion: "2", incomingTexts: "nope", fragments: [], insertions: [] }),
    "utf8",
  );
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await fetch(`${baseUrl}/api/manifest`);
    assert.equal(response.status, 500);
    const body = (await response.json()) as { error: string; code: string };
    assert.equal(body.code, "INVALID_MANIFEST");
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("a missing library file is a named 404, not a 400", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await fetch(
      `${baseUrl}/api/library/content?path=${encodeURIComponent("manjka.md")}`,
    );
    assert.equal(response.status, 404);
    const body = (await response.json()) as { error: string };
    assert.match(body.error, /File not found in library/);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("fragmentPointId is deterministic: re-indexing replaces instead of duplicating", () => {
  const first = fragmentPointId("fragment-0001");
  assert.match(first, /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
  assert.equal(first, fragmentPointId("fragment-0001"));
  assert.notEqual(first, fragmentPointId("fragment-0002"));
});

test("withManifestLock serializes concurrent manifest writes per project root", async () => {
  const projectRoot = await createTempDirectory();
  const events: string[] = [];
  let releaseFirst!: () => void;

  const first = withManifestLock(projectRoot, () => new Promise<void>((resolveOperation) => {
    releaseFirst = () => {
      events.push("first-done");
      resolveOperation();
    };
  }));
  const second = withManifestLock(projectRoot, async () => {
    events.push("second-started");
  });

  // The second operation must not start while the first still holds the lock.
  assert.deepEqual(events, []);

  releaseFirst();
  await first;
  await second;
  assert.deepEqual(events, ["first-done", "second-started"]);

  await cleanupTempDirectory(projectRoot);
});

test("degraded 502 responses name the failure cause instead of swallowing it", async () => {
  const projectRoot = await createTempDirectory();
  // A closed port forces the Ollama fetch to fail fast without network deps.
  const server = startWorkbenchApiServer(projectRoot, 0, { ollamaUrl: "http://127.0.0.1:1" });
  const baseUrl = await waitForBaseUrl(server);

  try {
    const degraded = await postJson<{ ok: boolean; cause: string }>(`${baseUrl}/api/suggestions`, {
      text: "Odlomek o bistvu.",
    });
    assert.equal(degraded.status, 502);
    assert.equal(degraded.body.ok, false);
    assert.ok(typeof degraded.body.cause === "string" && degraded.body.cause.length > 0);
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
  return mkdtemp(join(tmpdir(), "atmavictu-hardening-"));
}

async function cleanupTempDirectory(projectRoot: string): Promise<void> {
  await rm(projectRoot, { force: true, recursive: true });
}

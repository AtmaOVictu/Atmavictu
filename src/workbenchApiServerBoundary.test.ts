import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { AddressInfo } from "node:net";
import test from "node:test";

import { startWorkbenchApiServer } from "./workbenchApiServer.js";

test("path traversal out of the library root is refused with a named 400", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const escapeResponse = await fetch(
      `${baseUrl}/api/library/content?path=${encodeURIComponent("../evil.md")}`,
    );
    assert.equal(escapeResponse.status, 400);
    const escape = (await escapeResponse.json()) as { error: string };
    assert.match(escape.error, /must stay within its root/);

    const absoluteResponse = await fetch(
      `${baseUrl}/api/library/content?path=${encodeURIComponent("/etc/passwd")}`,
    );
    assert.equal(absoluteResponse.status, 400);
    const absolute = (await absoluteResponse.json()) as { error: string };
    assert.match(absolute.error, /must be a relative path/);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("library listing ignores workbench internals and walks nested directories", async () => {
  const projectRoot = await createTempDirectory();
  await writeFile(join(projectRoot, "a.md"), "# A", "utf8");
  await mkdir(join(projectRoot, "nested", "dir"), { recursive: true });
  await writeFile(join(projectRoot, "nested", "dir", "b.md"), "# B", "utf8");
  await mkdir(join(projectRoot, "node_modules"), { recursive: true });
  await writeFile(join(projectRoot, "node_modules", "x.js"), "module.exports = {};", "utf8");
  await mkdir(join(projectRoot, ".git"), { recursive: true });
  await writeFile(join(projectRoot, ".git", "config"), "[core]", "utf8");
  // A real, valid empty manifest: an invalid one would poison every route
  // that calls ensureManifestFile — this test must protect, not corrupt.
  await writeFile(
    join(projectRoot, "book.workbench.json"),
    JSON.stringify({ manifestVersion: "2", incomingTexts: [], fragments: [], insertions: [] }),
    "utf8",
  );

  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await fetch(`${baseUrl}/api/library`);
    assert.equal(response.status, 200);
    const entries = (await response.json()) as Array<{ path: string; captured: boolean }>;
    assert.deepEqual(
      entries.map((entry) => entry.path),
      ["a.md", "nested/dir/b.md"],
    );
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

test("extra library names delo-artifact provenance when the envelope is present", async () => {
  const projectRoot = await createTempDirectory();
  const extraRoot = await createTempDirectory();
  await writeFile(
    join(extraRoot, "artefakt.md"),
    '<!-- delo-artifact:v1{"artifact_id":"art-0001","output_type":"/seciraj","next_action":"razrezi","created_at":"2026-11-08T00:00:00Z"} -->\nVsebina.',
    "utf8",
  );
  await writeFile(join(extraRoot, "navadno.md"), "Navadna vsebina brez ovojnice.", "utf8");

  const server = startWorkbenchApiServer(projectRoot, 0, { extraLibraryRoot: extraRoot });
  const baseUrl = await waitForBaseUrl(server);

  try {
    const response = await fetch(`${baseUrl}/api/library/extra`);
    assert.equal(response.status, 200);
    const entries = (await response.json()) as Array<{
      path: string;
      deloProvenance: { artifactId: string; outputType: string; nextAction?: string; createdAt?: string } | null;
    }>;
    const byPath = new Map(entries.map((entry) => [entry.path, entry]));
    assert.ok(byPath.has("artefakt.md"));
    assert.ok(byPath.has("navadno.md"));
    assert.deepEqual(byPath.get("artefakt.md")?.deloProvenance, {
      artifactId: "art-0001",
      outputType: "/seciraj",
      nextAction: "razrezi",
      createdAt: "2026-11-08T00:00:00Z",
    });
    assert.equal(byPath.get("navadno.md")?.deloProvenance, null);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
    await cleanupTempDirectory(extraRoot);
  }
});

test("extra library without a configured root is a named 404", async () => {
  const projectRoot = await createTempDirectory();
  const server = startWorkbenchApiServer(projectRoot, 0);
  const baseUrl = await waitForBaseUrl(server);

  try {
    const listing = await fetch(`${baseUrl}/api/library/extra`);
    assert.equal(listing.status, 404);
    const body = (await listing.json()) as { error: string };
    assert.match(body.error, /No extraLibraryRoot configured/);

    const content = await fetch(`${baseUrl}/api/library/extra/content?path=x.md`);
    assert.equal(content.status, 404);
  } finally {
    server.close();
    await cleanupTempDirectory(projectRoot);
  }
});

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
  return mkdtemp(join(tmpdir(), "atmavictu-boundary-"));
}

async function cleanupTempDirectory(projectRoot: string): Promise<void> {
  await rm(projectRoot, { force: true, recursive: true });
}

import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

/**
 * Ure in prijema — VBL §0.30 × 10² (štiri prijema, dve uri, en dih)
 * in §0.20 × 10² (izmerjeno pri viru, never from memory).
 *
 * Seal je ločen iz Manifest-a (schema v2 je `additionalProperties: false`),
 * živi ob njim kot `book.workbench.seal.json`: delo in priča o delu.
 */

export interface ManifestClock {
  sealedAt: string;        // system wall-clock at seal time
  receivedAt: string | null; // receiver's clock (§0.30: completion witnessed by receiver)
  gitHead?: string;        // HEAD ref/SHA, če je citljiv
  ci: boolean;             // CI environment
  cli: boolean;            // CLI session
}

export interface FourReceipts {
  manifest: boolean; // book.workbench.json written
  seal: boolean;     // book.workbench.seal.json written
  cli: boolean;      // CLI output emitted
  ci: boolean;       // CI artifact emitted
}

export interface ManifestSeal {
  manifestPath: string;
  manifestSha256: string;
  receipts: FourReceipts;
  clock: ManifestClock;
  scar?: string; // named fall reference (§0.2 × 10¹), če obstaja
}

export function nowIso(): string {
  return new Date().toISOString();
}

/**
 * Prebere git HEAD (ref ali ločeni SHA). Vrne undefined, če .git ni dostopen.
 */
export async function readGitHead(root: string): Promise<string | undefined> {
  try {
    const head = await readFile(join(root, ".git", "HEAD"), "utf8");
    const refMatch = head.match(/^ref: (.+)\s*$/);
    const ref = refMatch?.[1];
    if (ref) {
      const refPath = join(root, ".git", ...ref.split("/"));
      try {
        return (await readFile(refPath, "utf8")).trim();
      } catch {
        // neuspešno — vrnemo glavo same datoteke
      }
    }
    return head.trim();
  } catch {
    return undefined;
  }
}

export function fourReceipts(opts: {
  cli?: boolean;
  ci?: boolean;
} = {}): FourReceipts {
  return {
    manifest: true,
    seal: true,
    cli: opts.cli === true,
    ci: opts.ci === true,
  };
}

export function manifestSha256(manifest: unknown): string {
  return createHash("sha256").update(JSON.stringify(manifest)).digest("hex");
}

/**
 * Zapiše seal obhajajo manifestu. Vsaka mutacija dela (capture, insert, …)
 * bi ga morala zaviti — ta funkcija je jedira; klicajoči naj določi cli/ci.
 */
export async function writeSeal(
  projectRoot: string,
  manifest: unknown,
  opts: { cli?: boolean; ci?: boolean; scar?: string } = {},
): Promise<ManifestSeal> {
  const manifestPath = resolve(join(projectRoot, "book.workbench.json"));
  const sealPath = resolve(join(projectRoot, "book.workbench.seal.json"));

  const clock: ManifestClock = {
    sealedAt: nowIso(),
    receivedAt: null,
    ci: process.env.CI === "true",
    cli: opts.cli === true,
  };
  const gitHead = await readGitHead(projectRoot);
  if (gitHead) {
    clock.gitHead = gitHead;
  }

  const seal: ManifestSeal = {
    manifestPath,
    manifestSha256: manifestSha256(manifest),
    receipts: fourReceipts({ cli: opts.cli === true, ci: opts.ci === true }),
    clock,
    ...(opts.scar ? { scar: opts.scar } : {}),
  };

  const sealJson = `${JSON.stringify(seal, null, 2)}\n`;
  await writeFile(sealPath, sealJson, "utf8");
  return seal;
}

/**
 * Preberi seal, če obstaja.
 */
export async function readSeal(projectRoot: string): Promise<ManifestSeal | null> {
  try {
    const raw = await readFile(join(projectRoot, "book.workbench.seal.json"), "utf8");
    return JSON.parse(raw) as ManifestSeal;
  } catch {
    return null;
  }
}

/**
 * Prejemnik potrjuje prejem seal-a (receiver's clock, §0.30).
 */
export function confirmReceipt(seal: ManifestSeal): ManifestSeal {
  return {
    ...seal,
    clock: { ...seal.clock, receivedAt: nowIso() },
  };
}

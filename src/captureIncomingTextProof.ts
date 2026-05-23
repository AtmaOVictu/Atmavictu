import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

import {
  captureIncomingText,
  createCaptureIncomingTextConsequence,
  renderCaptureIncomingTextConsequence,
} from "./workbenchManifestRepository.js";

const DEFAULT_TITLE = "Proof Capture";
const DEFAULT_BODY = "Dokazni vhod za captureIncomingText.";

export interface CaptureIncomingTextProofOptions {
  projectRoot: string;
  title: string;
  body: string;
}

export function parseCaptureIncomingTextProofArgs(
  argv: readonly string[],
): CaptureIncomingTextProofOptions {
  const [projectRoot, title, body, ...rest] = argv;

  if (projectRoot === undefined || projectRoot.trim().length === 0) {
    throw new Error(
      "Usage: node build/src/captureIncomingTextProof.js <projectRoot> [title] [body]",
    );
  }

  if (rest.length > 0) {
    throw new Error(
      "captureIncomingTextProof accepts at most three arguments: <projectRoot> [title] [body]",
    );
  }

  return {
    projectRoot,
    title: normalizeCliValue(title) ?? DEFAULT_TITLE,
    body: normalizeCliValue(body) ?? DEFAULT_BODY,
  };
}

export async function runCaptureIncomingTextProof(
  options: CaptureIncomingTextProofOptions,
): Promise<string> {
  const result = await captureIncomingText(options.projectRoot, {
    title: options.title,
    body: options.body,
  });
  const consequence = createCaptureIncomingTextConsequence(result);

  return renderCaptureIncomingTextConsequence(consequence);
}

function normalizeCliValue(value: string | undefined): string | undefined {
  if (value === undefined) {
    return undefined;
  }

  const normalizedValue = value.trim();
  return normalizedValue.length > 0 ? normalizedValue : undefined;
}

async function main(): Promise<void> {
  const options = parseCaptureIncomingTextProofArgs(process.argv.slice(2));
  const output = await runCaptureIncomingTextProof(options);
  process.stdout.write(`${output}\n`);
}

function isDirectExecution(): boolean {
  const entryPath = process.argv[1];
  if (entryPath === undefined) {
    return false;
  }

  return resolve(entryPath) === fileURLToPath(import.meta.url);
}

if (isDirectExecution()) {
  try {
    await main();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`${message}\n`);
    process.exitCode = 1;
  }
}

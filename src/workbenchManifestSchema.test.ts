import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

interface JsonSchemaObject {
  $defs?: Record<string, unknown>;
  properties?: Record<string, unknown>;
  additionalProperties?: boolean;
  type?: string;
  pattern?: string;
  allOf?: unknown[];
  not?: {
    pattern?: string;
  };
}

test("schema reuses non-blank and path string definitions for manifest fields", async () => {
  const schemaPath = new URL("../../schema/workbench.manifest.v1.schema.json", import.meta.url);
  const schema = JSON.parse(await readFile(schemaPath, "utf8")) as JsonSchemaObject;
  const defs = schema.$defs as Record<string, JsonSchemaObject>;
  const incomingText = defs.IncomingText!;
  const fragment = defs.Fragment!;
  const insertion = defs.Insertion!;
  const concept = defs.Concept!;

  assert.equal(defs.NonBlankString?.type, "string");
  assert.equal(defs.NonBlankString?.pattern, "\\S");
  assert.deepEqual(defs.PathString?.allOf, [
    { $ref: "#/$defs/NonBlankString" },
    { not: { pattern: "^(?:[\\\\/]|[A-Za-z]:[\\\\/])" } },
    { not: { pattern: "(?:^|[\\\\/])\\.\\.(?:[\\\\/]|$)" } },
  ]);

  assert.equal((incomingText.properties?.id as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((incomingText.properties?.sourcePath as { $ref?: string }).$ref, "#/$defs/PathString");
  assert.equal((fragment.properties?.id as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((fragment.properties?.incomingTextId as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((fragment.properties?.text as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((insertion.properties?.id as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((insertion.properties?.fragmentId as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((insertion.properties?.targetChapterPath as { $ref?: string }).$ref, "#/$defs/PathString");
  assert.equal((concept.properties?.id as { $ref?: string }).$ref, "#/$defs/NonBlankString");
  assert.equal((concept.properties?.label as { $ref?: string }).$ref, "#/$defs/NonBlankString");
});

test("schema PathString rejects absolute and traversal paths while allowing safe relative paths", async () => {
  const schemaPath = new URL("../../schema/workbench.manifest.v1.schema.json", import.meta.url);
  const schema = JSON.parse(await readFile(schemaPath, "utf8")) as JsonSchemaObject;
  const defs = schema.$defs as Record<string, JsonSchemaObject>;
  const pathString = defs.PathString!;
  const rules = pathString.allOf as JsonSchemaObject[];

  assert.equal(matchesPathString(defs, rules, "/tmp/file.txt"), false);
  assert.equal(matchesPathString(defs, rules, "C:\\Users\\Luka\\secret.txt"), false);
  assert.equal(matchesPathString(defs, rules, "C:/Users/Luka/secret.txt"), false);
  assert.equal(matchesPathString(defs, rules, "\\\\server\\share\\file.txt"), false);
  assert.equal(matchesPathString(defs, rules, "//server/share/chapter.md"), false);
  assert.equal(matchesPathString(defs, rules, "../secret.txt"), false);
  assert.equal(matchesPathString(defs, rules, "incoming/../../secret.txt"), false);
  assert.equal(matchesPathString(defs, rules, "incoming/incoming-0001.txt"), true);
  assert.equal(matchesPathString(defs, rules, "chapters/chapter-001.md"), true);
});

test("schema keeps optional metadata fields as plain strings", async () => {
  const schemaPath = new URL("../../schema/workbench.manifest.v1.schema.json", import.meta.url);
  const schema = JSON.parse(await readFile(schemaPath, "utf8")) as JsonSchemaObject;
  const defs = schema.$defs as Record<string, JsonSchemaObject>;
  const incomingText = defs.IncomingText!;
  const fragment = defs.Fragment!;
  const insertion = defs.Insertion!;
  const concept = defs.Concept!;

  assert.equal((incomingText.properties?.title as { type?: string }).type, "string");
  assert.equal((incomingText.properties?.note as { type?: string }).type, "string");
  assert.equal((fragment.properties?.title as { type?: string }).type, "string");
  assert.equal((fragment.properties?.note as { type?: string }).type, "string");
  assert.equal((insertion.properties?.positionNote as { type?: string }).type, "string");
  assert.equal((insertion.properties?.note as { type?: string }).type, "string");
  assert.equal((concept.properties?.note as { type?: string }).type, "string");
});

function matchesPathString(
  defs: Record<string, JsonSchemaObject>,
  rules: JsonSchemaObject[],
  pathValue: string,
): boolean {
  for (const rule of rules) {
    if ("$ref" in rule && typeof (rule as { $ref?: unknown }).$ref === "string") {
      const ref = (rule as { $ref: string }).$ref;
      const definitionName = ref.replace("#/$defs/", "");
      const definition = defs[definitionName];

      if (definition?.type === "string" && definition.pattern !== undefined) {
        if (!new RegExp(definition.pattern).test(pathValue)) {
          return false;
        }
      }

      continue;
    }

    if (rule.not?.pattern !== undefined && new RegExp(rule.not.pattern).test(pathValue)) {
      return false;
    }
  }

  return true;
}

import assert from "node:assert/strict";
import test from "node:test";

import {
  buildSuggestionPrompt,
  parseSuggestionResponse,
  SUGGESTION_MAX_INPUT_CHARS,
} from "./workbenchSuggestions.js";

test("parseSuggestionResponse extracts title and concepts from clean JSON", () => {
  const result = parseSuggestionResponse('{"title": "Bistvo", "concepts": ["Res", "Pot"]}');

  assert.equal(result.title, "Bistvo");
  assert.deepEqual(result.concepts, ["Res", "Pot"]);
});

test("parseSuggestionResponse tolerates prose wrapping the JSON", () => {
  const result = parseSuggestionResponse(
    'Here you go:\n{"title":"Koren","concepts":["A","B","C"]}\nHope that helps.',
  );

  assert.equal(result.title, "Koren");
  assert.deepEqual(result.concepts, ["A", "B", "C"]);
});

test("parseSuggestionResponse returns empty concepts for non-object or invalid input", () => {
  assert.deepEqual(parseSuggestionResponse(""), { concepts: [] });
  assert.deepEqual(parseSuggestionResponse("no json here"), { concepts: [] });
  assert.deepEqual(parseSuggestionResponse("not valid json {"), { concepts: [] });
});

test("parseSuggestionResponse trims and caps concepts, drops non-strings", () => {
  const result = parseSuggestionResponse(
    '{"concepts": ["  a  ", "", 42, "b", "c", "d", "e", "f"]}',
  );

  assert.equal(result.concepts.length, 5);
  assert.deepEqual(result.concepts, ["a", "b", "c", "d", "e"]);
});

test("parseSuggestionResponse omits title when absent or blank", () => {
  const noTitle = parseSuggestionResponse('{"concepts": ["A"]}');
  assert.equal(noTitle.title, undefined);
  assert.deepEqual(noTitle.concepts, ["A"]);

  const blankTitle = parseSuggestionResponse('{"title": "   ", "concepts": []}');
  assert.equal(blankTitle.title, undefined);
});

test("buildSuggestionPrompt includes the excerpt and caps it", () => {
  const result = buildSuggestionPrompt("x".repeat(SUGGESTION_MAX_INPUT_CHARS + 500));

  assert.match(result, /Respond ONLY with a JSON object/);
  // the excerpt is capped, so the whole prompt is not unbounded
  assert.ok(result.length < SUGGESTION_MAX_INPUT_CHARS + 2000);
});
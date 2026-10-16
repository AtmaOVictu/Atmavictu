/**
 * Pure helpers for LLM-assisted fragment suggestions (title + concepts).
 *
 * Kept separate from workbenchApiServer so the prompt-building and response
 * parsing are unit-testable without any network. The actual Ollama call lives
 * in the API server and uses these; on any failure the server degrades
 * gracefully (it never blocks the workbench on an unreachable model).
 */

export interface FragmentSuggestion {
  title?: string;
  concepts: string[];
}

export const SUGGESTION_MODEL = "qwen3:8b";
export const SUGGESTION_MAX_INPUT_CHARS = 2000;

export function buildSuggestionPrompt(text: string): string {
  const excerpt = text.slice(0, SUGGESTION_MAX_INPUT_CHARS).trim();
  return [
    "You are assisting in a Book Workbench. Given one short working excerpt (a fragment),",
    "suggest how to label it:",
    "1. title: a short Slovenian noun phrase (max ~8 words) naming the excerpt.",
    "2. concepts: 1-4 short Slovenian concept labels that group this excerpt thematically.",
    "",
    "The excerpt is:",
    excerpt,
    "",
    'Respond ONLY with a JSON object: {"title": "...", "concepts": ["...", "..."]}',
  ].join("\n");
}

/**
 * Tolerant parser: the model is asked for pure JSON, but may wrap it in prose
 * or emit trailing text. Extracts the first {...} object and validates fields.
 * Never throws; returns an empty suggestion on any failure.
 */
export function parseSuggestionResponse(raw: string): FragmentSuggestion {
  if (typeof raw !== "string" || raw.trim().length === 0) {
    return { concepts: [] };
  }

  const objectMatch = raw.match(/\{[\s\S]*\}/);
  if (objectMatch === null) {
    return { concepts: [] };
  }

  let parsed: Record<string, unknown>;
  try {
    parsed = JSON.parse(objectMatch[0]) as Record<string, unknown>;
  } catch {
    return { concepts: [] };
  }

  const title =
    typeof parsed.title === "string" && parsed.title.trim().length > 0 ? parsed.title.trim() : undefined;

  const concepts = Array.isArray(parsed.concepts)
    ? parsed.concepts
        .filter((concept): concept is string => typeof concept === "string")
        .map((concept) => concept.trim())
        .filter((concept) => concept.length > 0)
        .slice(0, 5)
    : [];

  return {
    ...(title !== undefined ? { title } : {}),
    concepts,
  };
}
/**
 * Pure helpers for Qdrant semantic search over fragments.
 *
 * Kept separate from workbenchApiServer so the payload-building and response
 * parsing are unit-testable without any network. The actual Ollama/Qdrant
 * HTTP calls live in the API server; on any failure it degrades gracefully
 * (never blocks the workbench on unreachable services).
 */

export interface QdrantSearchHit {
  fragmentId: string;
  title?: string;
  text: string;
  score: number;
}

export const EMBEDDING_MODEL = "bge-m3";
export const QDRANT_COLLECTION = "workbench_fragments";
export const EMBEDDING_DIMENSIONS = 1024;

/** Build the Ollama /api/embed request body. */
export function buildEmbeddingRequest(text: string): { model: string; input: string } {
  return { model: EMBEDDING_MODEL, input: text.slice(0, 2000) };
}

/** Tolerant embedding parser; returns an empty vector on any failure. */
export function parseEmbeddingResponse(raw: unknown): number[] {
  if (!isRecord(raw)) {
    return [];
  }
  const embeddings = raw.embeddings;
  if (Array.isArray(embeddings) && Array.isArray(embeddings[0]) && isFiniteArray(embeddings[0])) {
    return embeddings[0] as number[];
  }
  const embedding = raw.embedding;
  if (Array.isArray(embedding) && isFiniteArray(embedding)) {
    return embedding as number[];
  }
  return [];
}

/** Build the Qdrant collection-create body (idempotent). */
export function buildQdrantCollectionBody(size: number): { vectors: { size: number; distance: string } } {
  return { vectors: { size, distance: "Cosine" } };
}

/** Build the Qdrant points upsert body. */
export function buildQdrantUpsertBody(
  points: Array<{ id: string; vector: number[]; payload: Record<string, unknown> }>,
): { points: Array<{ id: string; vector: number[]; payload: Record<string, unknown> }> } {
  return { points };
}

/** Build the Qdrant search body. */
export function buildQdrantSearchBody(
  vector: number[],
  limit: number,
): { vector: number[]; limit: number; with_payload: boolean } {
  return { vector, limit, with_payload: true };
}

/** Parse a Qdrant search response into normalized hits. */
export function parseQdrantSearchResponse(raw: unknown): QdrantSearchHit[] {
  if (!isRecord(raw) || !Array.isArray(raw.result)) {
    return [];
  }
  const hits: QdrantSearchHit[] = [];
  for (const hit of raw.result) {
    if (!isRecord(hit) || typeof hit.score !== "number" || !isRecord(hit.payload)) {
      continue;
    }
    const fragmentId = typeof hit.payload.fragmentId === "string" ? hit.payload.fragmentId : "";
    const text = typeof hit.payload.text === "string" ? hit.payload.text : "";
    if (fragmentId.length === 0) {
      continue;
    }
    const title = typeof hit.payload.title === "string" ? hit.payload.title : undefined;
    hits.push({
      fragmentId,
      ...(title ? { title } : {}),
      text,
      score: hit.score,
    });
  }
  return hits;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isFiniteArray(value: unknown[]): value is number[] {
  return value.every((item) => typeof item === "number" && Number.isFinite(item));
}
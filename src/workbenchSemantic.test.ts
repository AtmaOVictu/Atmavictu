import assert from "node:assert/strict";
import test from "node:test";

import {
  buildEmbeddingRequest,
  buildQdrantCollectionBody,
  buildQdrantSearchBody,
  buildQdrantUpsertBody,
  EMBEDDING_DIMENSIONS,
  EMBEDDING_MODEL,
  parseEmbeddingResponse,
  parseQdrantSearchResponse,
  QDRANT_COLLECTION,
} from "./workbenchSemantic.js";

test("buildEmbeddingRequest uses the bge-m3 model", () => {
  const request = buildEmbeddingRequest("Odlomek o bistvu.");

  assert.equal(request.model, EMBEDDING_MODEL);
  assert.equal(request.input, "Odlomek o bistvu.");
});

test("parseEmbeddingResponse extracts the vector from embeddings or embedding", () => {
  const viaEmbeddings = parseEmbeddingResponse({ embeddings: [[0.1, 0.2, 0.3]] });
  assert.deepEqual(viaEmbeddings, [0.1, 0.2, 0.3]);

  const viaEmbedding = parseEmbeddingResponse({ embedding: [0.5, 0.6] });
  assert.deepEqual(viaEmbedding, [0.5, 0.6]);
});

test("parseEmbeddingResponse returns empty for junk input", () => {
  assert.deepEqual(parseEmbeddingResponse(null), []);
  assert.deepEqual(parseEmbeddingResponse({}), []);
  assert.deepEqual(parseEmbeddingResponse({ embeddings: [[]] }), []);
  assert.deepEqual(parseEmbeddingResponse({ embeddings: [["a"]] }), []);
});

test("buildQdrantCollectionBody uses the embedding dimensions and cosine distance", () => {
  const body = buildQdrantCollectionBody(EMBEDDING_DIMENSIONS);

  assert.equal(body.vectors.size, 1024);
  assert.equal(body.vectors.distance, "Cosine");
  assert.equal(QDRANT_COLLECTION, "workbench_fragments");
});

test("buildQdrantUpsertBody and buildQdrantSearchBody shape the payloads", () => {
  const upsert = buildQdrantUpsertBody([
    { id: "fragment-0001", vector: [1], payload: { fragmentId: "fragment-0001", text: "x" } },
  ]);
  assert.equal(upsert.points.length, 1);
  assert.equal(upsert.points[0]?.id, "fragment-0001");

  const search = buildQdrantSearchBody([1, 2], 5);
  assert.deepEqual(search, { vector: [1, 2], limit: 5, with_payload: true });
});

test("parseQdrantSearchResponse normalizes hits and drops malformed ones", () => {
  const raw = {
    result: [
      { id: "fragment-0001", score: 0.92, payload: { fragmentId: "fragment-0001", title: "Bistvo", text: "Odlomek" } },
      { id: "fragment-0002", score: 0.5, payload: { fragmentId: "fragment-0002", text: "Drugi" } },
      { score: 0.1, payload: {} },
    ],
  };

  const hits = parseQdrantSearchResponse(raw);

  assert.equal(hits.length, 2);
  assert.equal(hits[0]?.fragmentId, "fragment-0001");
  assert.equal(hits[0]?.title, "Bistvo");
  assert.equal(hits[0]?.score, 0.92);
  assert.equal(hits[1]?.title, undefined);
});

test("parseQdrantSearchResponse returns empty for junk input", () => {
  assert.deepEqual(parseQdrantSearchResponse(null), []);
  assert.deepEqual(parseQdrantSearchResponse({}), []);
  assert.deepEqual(parseQdrantSearchResponse({ result: "nope" }), []);
});
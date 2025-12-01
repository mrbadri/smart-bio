// lib/embeddings.ts
import OpenAI from "openai";
import type { TextChunk } from "./chunk";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

const EMBEDDING_MODEL = "text-embedding-3-small";

export type ChunkEmbedding = {
  chunk: TextChunk;
  embedding: number[];
};

export async function embedChunks(
  chunks: TextChunk[],
  batchSize = 64
): Promise<ChunkEmbedding[]> {
  const result: ChunkEmbedding[] = [];

  for (let i = 0; i < chunks.length; i += batchSize) {
    const slice = chunks.slice(i, i + batchSize);
    const inputs = slice.map((c) => c.text);

    const resp = await client.embeddings.create({
      model: EMBEDDING_MODEL,
      input: inputs,
    });

    resp.data.forEach((item, idx) => {
      result.push({
        chunk: slice[idx],
        embedding: item.embedding,
      });
    });
  }

  return result;
}

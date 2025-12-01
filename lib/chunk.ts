// lib/chunk.ts
export type TextChunk = {
  index: number;
  start: number; // offset شروع در استرینگ اصلی (اختیاری ولی مفید)
  end: number; // offset پایان
  text: string;
};

export function chunkText(
  text: string,
  options?: {
    chunkSize?: number; // تقریبی بر اساس کاراکتر
    overlap?: number;
  }
): TextChunk[] {
  const chunkSize = options?.chunkSize ?? 1200;
  const overlap = options?.overlap ?? 200;

  const cleaned = text.replace(/\s+/g, " ").trim();
  const chunks: TextChunk[] = [];

  let start = 0;
  let index = 0;

  while (start < cleaned.length) {
    const end = start + chunkSize;
    const slice = cleaned.slice(start, end).trim();
    if (slice.length > 0) {
      chunks.push({
        index,
        start,
        end: Math.min(end, cleaned.length),
        text: slice,
      });
      index++;
    }
    start = end - overlap;
    if (start < 0) start = 0;
  }

  return chunks;
}

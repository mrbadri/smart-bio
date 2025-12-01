// vector-prep.ts

export type RawPage = {
  content: string;
  page: number;
  chapter?: string | null;
  lecture?: string | null;
};

export type VectorDoc = {
  id: string;
  text: string;
  metadata: {
    page_start: number;
    page_end: number;
    chapter?: string;
    lecture?: string;
    chunk_index: number;
    source?: string;
    lang: "fa";
  };
};

export type PrepOptions = {
  // chunking
  chunkSizeChars?: number; // default 1200
  chunkOverlapChars?: number; // default 200
  minChunkChars?: number; // default 80

  // cleanup
  dropShortLinesUnder?: number; // default 10
  dropHeadingLines?: boolean; // default true
  dropDuplicateLines?: boolean; // default true

  // metadata
  sourceName?: string; // e.g. "bio10_pdf"
};

/* ----------------------------- 1) Raw clean ----------------------------- */

const CONTROL_CHARS = /[\u0000-\u001F\u007F\b]/g; // includes \b
const MULTI_SPACE = /\s+/g;

export function rawClean(text: string): string {
  if (!text) return "";
  return text.replace(CONTROL_CHARS, " ").replace(MULTI_SPACE, " ").trim();
}

/* ------------------------- 2) Persian normalize ------------------------- */

const ARABIC_TO_PERSIAN_MAP: Record<string, string> = {
  ي: "ی",
  ك: "ک",
  ة: "ه",
  ؤ: "و",
  إ: "ا",
  أ: "ا",
  ٱ: "ا",
};

const ARABIC_DIACRITICS = /[\u064B-\u065F\u0670\u06D6-\u06ED]/g; // harakat
const TATWEEL = /\u0640/g; // ـ

export function normalizePersian(text: string): string {
  let t = text;

  for (const [a, p] of Object.entries(ARABIC_TO_PERSIAN_MAP)) {
    t = t.replaceAll(a, p);
  }

  t = t
    .replace(ARABIC_DIACRITICS, "")
    .replace(TATWEEL, "")
    // normalize punctuation spacing
    .replace(/\s*([،؛:!?])\s*/g, "$1 ")
    .replace(/\s*([.])\s*/g, ". ")
    .replace(/\s+/g, " ")
    .trim();

  return t;
}

/* -------------------- 3) Drop low-value / noisy lines ------------------- */

// headings / boilerplate you usually don't want alone in RAG:
const BAD_HEADING_LINE =
  /^(بیشتر بدانید|فعّالیت\s*\d+|شکل\s*\d+|شناسیواژه|مطالعۀ بیشتر|تمرین\s*\d+)\s*$/;

function dropLowValueLines(
  text: string,
  opts: Required<
    Pick<
      PrepOptions,
      "dropShortLinesUnder" | "dropHeadingLines" | "dropDuplicateLines"
    >
  >
): string {
  const rawLines = text
    .split(/[\n\r]+/)
    .map((l) => l.trim())
    .filter(Boolean);

  const seen = new Set<string>();
  const kept: string[] = [];

  for (const line of rawLines) {
    if (line.length < opts.dropShortLinesUnder) continue;
    if (opts.dropHeadingLines && BAD_HEADING_LINE.test(line)) continue;

    if (opts.dropDuplicateLines) {
      const key = line.replace(/\s+/g, " ");
      if (seen.has(key)) continue;
      seen.add(key);
    }

    kept.push(line);
  }

  return kept.join("\n");
}

/* ------------------------------- 4) Chunking ---------------------------- */

// character-based chunking with overlap (good default for embeddings)
export function chunkText(
  text: string,
  size = 1200,
  overlap = 200,
  minSize = 80
): string[] {
  const chunks: string[] = [];
  let i = 0;

  while (i < text.length) {
    const chunk = text.slice(i, i + size).trim();
    if (chunk.length >= minSize) chunks.push(chunk);
    i += Math.max(1, size - overlap);
  }

  return chunks;
}

/* -------------------------- 5) Main prep function ------------------------ */

export function prepareForVectorDB(
  pages: RawPage[],
  options: PrepOptions = {}
): VectorDoc[] {
  const opts = {
    chunkSizeChars: options.chunkSizeChars ?? 1200,
    chunkOverlapChars: options.chunkOverlapChars ?? 200,
    minChunkChars: options.minChunkChars ?? 80,
    dropShortLinesUnder: options.dropShortLinesUnder ?? 10,
    dropHeadingLines: options.dropHeadingLines ?? true,
    dropDuplicateLines: options.dropDuplicateLines ?? true,
    sourceName: options.sourceName ?? "bio_pdf",
  };

  const docs: VectorDoc[] = [];

  for (const p of pages) {
    // pipeline
    const cleaned = dropLowValueLines(
      normalizePersian(rawClean(p.content)),
      opts
    );

    const chunks = chunkText(
      cleaned,
      opts.chunkSizeChars,
      opts.chunkOverlapChars,
      opts.minChunkChars
    );

    chunks.forEach((ch, idx) => {
      docs.push({
        id: `${opts.sourceName}:p${p.page}:c${idx}`,
        text: ch,
        metadata: {
          page_start: p.page,
          page_end: p.page,
          chapter: p.chapter ?? undefined,
          lecture: p.lecture ?? undefined,
          chunk_index: idx,
          source: opts.sourceName,
          lang: "fa",
        },
      });
    });
  }

  return docs;
}

/* ------------------------------ Example usage ---------------------------- */

/*
  import fs from "node:fs";
  import { prepareForVectorDB } from "./vector-prep";
  import raw from "./raw-pages.json";
  
  const docs = prepareForVectorDB(raw, {
    sourceName: "bio10_pdf",
    chunkSizeChars: 1300,
    chunkOverlapChars: 220,
  });
  
  fs.writeFileSync("vector-docs.json", JSON.stringify(docs, null, 2), "utf-8");
  console.log("docs count:", docs.length);
  */

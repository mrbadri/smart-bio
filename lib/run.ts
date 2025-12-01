import { chunkText } from "./chunk";
import { readFile, writeFile } from "fs/promises";
import { embedChunks } from "./embeding";
import { pdfParser } from "./pdf-parser-v1";
import { getChapterAndLectureByPage } from "./get-chapter";
import { BIOLOGY_TEXTBOOK } from "@/constant/bio";
import { pageParser } from "./page-parser";
import { prepareForVectorDB } from "./vector-prep";

const run = async () => {
  //  Read File
  const { pages } = await pdfParser();
  const res = pageParser(pages);

  //   const res = getChapterAndLectureByPage(3, BIOLOGY_TEXTBOOK);
  await writeFile("page-parsed.json", JSON.stringify(res, null, 2));
  console.log(res);

  const raw = await readFile("page-parsed.json", "utf-8");

  const docs = prepareForVectorDB(JSON.parse(raw), {
    sourceName: "bio10_pdf",
    chunkSizeChars: 1300,
    chunkOverlapChars: 220,
  });

  await writeFile("vector-prepared.json", JSON.stringify(docs, null, 2));
};

run();

const docString = await readFile("text-v1.txt", "utf-8");

const chunks = chunkText(docString, {
  chunkSize: 1200,
  overlap: 200,
});

// console.log(chunks);

// save in json file
// await writeFile("chunks.json", JSON.stringify(chunks, null, 2));
const vectors = await embedChunks(chunks, 64);

// save in json file
await writeFile("vectors.json", JSON.stringify(vectors, null, 2));

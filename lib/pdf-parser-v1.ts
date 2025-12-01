// lib/pdf.ts
import { writeFile } from "fs/promises";
import { PDFParse, type TextResult } from "pdf-parse";

export const pdfParser = async (): Promise<TextResult> => {
  const pdfPath = "bio-10-v1.pdf";
  // Create parser instance
  const parser = new PDFParse({ url: pdfPath });

  const result = await parser.getText();

  //  write a file json
  // for result.pages
  //   i want write result.pages in json file
  await writeFile("pages.json", JSON.stringify(result.pages, null, 2));

  return result;
};

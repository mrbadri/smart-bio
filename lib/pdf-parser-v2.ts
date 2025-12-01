import { extractImages, extractText, getDocumentProxy } from "unpdf";
import { readFile, writeFile } from "fs/promises";
import sharp from "sharp";

async function run() {
  const pdfPath = "bio-10.pdf";

  const buffer = await readFile("./bio-10-v1.pdf");

  // Then, load the PDF file into a PDF.js document
  const pdf = await getDocumentProxy(new Uint8Array(buffer));

  //    IMAGE:
  //   const imagesData = await extractImages(pdf, 4);
  //   console.log(`Found ${imagesData.length} images on page 1`);

  //   // Process each image with sharp (optional)
  //   let totalImagesProcessed = 0;
  //   for (const imgData of imagesData) {
  //     const imageIndex = ++totalImagesProcessed;

  //     await sharp(imgData.data, {
  //       raw: {
  //         width: imgData.width,
  //         height: imgData.height,
  //         channels: imgData.channels,
  //       },
  //     })
  //       .png()
  //       .toFile(`image-${imageIndex}.png`);

  //     console.log(
  //       `Saved image ${imageIndex} (${imgData.width}x${imgData.height}, ${imgData.channels} channels)`
  //     );
  //   }

  // Finally, extract the text from the PDF file
  const { totalPages, text } = await extractText(pdf, { mergePages: true });

  console.log(`Total pages: ${totalPages}`);
  console.log(text);
  //    write test in a file
  await writeFile("text.txt", text);
}

run();

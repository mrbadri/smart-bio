from llama_cloud_services import LlamaParse

parser = LlamaParse(
  # See how to get your API key at https://developers.llamaindex.ai/python/cloud/general/api_key/
  api_key="llx-XBtyThevmRXlr43daJL7KZkax3NRFKvLl8BC5LXTTaHIaSln",

  # The maximum number of pages to parse
  max_pages=25,

  # The parsing mode
  parse_mode="parse_page_with_llm",

  # The model to use
  model="openai-gpt-4-1-mini",

  # Whether to use high resolution OCR (Slow)
  high_res_ocr=True,

  # Adaptive long table. LlamaParse will try to detect long table and adapt the output
  adaptive_long_table=True,

  # Whether to try to extract outlined tables
  outlined_table_extraction=True,

  # Whether to output tables as HTML in the markdown output
  output_tables_as_HTML=True,

  # Whether to use precise bounding box extraction (experimental)
  precise_bounding_box=True,

  # The page separator
  page_separator="\n\n---\n\n",

  # The append to system prompt
  system_prompt_append="Only extract images that are non-text figures (photos, diagrams, charts).\r\nIf a region contains mostly text (Persian/Arabic/English), do NOT treat it as an image; OCR it as text instead.\r\nNever output an image for pure text blocks.",
  replace_failed_page_mode="raw_text",
)



# Example usage:

# sync
result = parser.parse("./input.pdf")

# # sync batch
# results = parser.parse(["./my_file1.pdf", "./my_file2.pdf"])

# # async
# result = await parser.aparse("./my_file.pdf")

# # async batch
# results = await parser.aparse(["./my_file1.pdf", "./my_file2.pdf"])

# get the llama-index markdown documents
markdown_documents = result.get_markdown_documents(split_by_page=True)

# get the llama-index text documents
text_documents = result.get_text_documents(split_by_page=False)

# get the image documents
image_documents = result.get_image_documents(
    include_screenshot_images=True,
    include_object_images=True,  # Changed to True to download extracted images
    # Optional: download the images to a directory
    # (default is to return the image bytes in ImageDocument objects)
    image_download_dir="./images",
)

# Iterate over image documents to ensure they are downloaded
print(f"\n--- Downloaded {len(image_documents)} images ---")
for i, img_doc in enumerate(image_documents):
    print(f"Image {i}: {img_doc.metadata}")

# access the raw job result
# Items will vary based on the parser configuration
for page in result.pages:
    print(page.text)
    print(page.md)
    print(page.images)
    print(page.layout)
    print(page.structuredData)
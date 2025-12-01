from llama_cloud_services import LlamaParse
import json
parser = LlamaParse(
  api_key="llx-XBtyThevmRXlr43daJL7KZkax3NRFKvLl8BC5LXTTaHIaSln",

  # The maximum number of pages to parse
  max_pages=25,

  # The parsing mode
  parse_mode="parse_page_with_agent",

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
#   languages=[
#   "fa",
#   "en"
# ],

  # The append to system prompt
  system_prompt_append="Only extract images that are non-text figures (photos, diagrams, charts).\r\nIf a region contains mostly text (Persian/Arabic/English), do NOT treat it as an image; OCR it as text instead.\r\nNever output an image for pure text blocks.",
  replace_failed_page_mode="raw_text",
)



parserImages = LlamaParse(
  # See how to get your API key at https://developers.llamaindex.ai/python/cloud/general/api_key/
  api_key="llx-XBtyThevmRXlr43daJL7KZkax3NRFKvLl8BC5LXTTaHIaSln",

  # The maximum number of pages to parse
  max_pages=25,

  # The parsing mode
  parse_mode="parse_page_with_llm",

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
result = parser.parse("./input.pdf");
resultImages = parserImages.parse("./input.pdf")

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
# get the image documents
image_documents = resultImages.get_image_documents(
    include_screenshot_images=True,
    include_object_images=True,
    # Optional: download the images to a directory
    # (default is to return the image bytes in ImageDocument objects)
    image_download_dir="./images",
)

#  save the markdown documents in a file
with open("markdown_documents.md", "w", encoding="utf-8") as f:
    for doc in markdown_documents:
        f.write(doc.text)
        f.write("\n\n")
    # f.write(image_documents)
    
    
# print(image_documents)
    



# result to json - manually construct dictionary from result
json_result = {
    "pages": {}
}
for i, page in enumerate(result.pages, 1):
    # Get images for this page from resultImages
    page_images = []
    for img_doc in image_documents:
        if hasattr(img_doc, 'metadata') and img_doc.metadata.get('page_number') == i:
            page_images.append({
                "image_path": img_doc.image_path if hasattr(img_doc, 'image_path') else None,
                "image_url": img_doc.image_url if hasattr(img_doc, 'image_url') else None,
                "text": img_doc.text if hasattr(img_doc, 'text') else None
            })
    
    page_data = {
        "page": i,
        "text": page.text,
        "md": page.md,
        "images": page_images,
        "layout": str(page.layout) if hasattr(page, 'layout') else None,
        "structuredData": page.structuredData if hasattr(page, 'structuredData') else None
    }
    json_result["pages"][str(i)] = page_data

#  now save the json result in a file
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(json_result, f, ensure_ascii=False, indent=2)

# access the raw job result
# Items will vary based on the parser configuration
for page in resultImages.pages:
    print(page.text)
    print(page.md)
    print(page.images)
    print(page.layout)
    print(page.structuredData)
    
    
    
    # i want store the result in a json file
    # with open("result.json", "w") as f:
    #     json.dump(result, f)

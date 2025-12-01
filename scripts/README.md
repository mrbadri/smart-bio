# PDF Parser Script

A clean, modular Python script for parsing PDF files using LlamaParse. Extracts text, markdown, images, and structured data from PDF documents with a professional, maintainable architecture.

## Features

- **Text Extraction**: Extract text content with high-quality OCR
- **Markdown Generation**: Convert PDF pages to markdown format
- **Image Extraction**: Extract figures, diagrams, and charts
- **Structured Output**: Generate JSON with page-level data
- **Chapter & Lecture Detection**: Automatic chapter and lecture identification for Persian biology textbook
- **Error Handling**: Comprehensive error handling and validation
- **Clean Architecture**: Modular design with separation of concerns
- **Configuration Management**: Centralized settings with environment variables
- **Type Safety**: Full type hints for better IDE support and error prevention
- **Flexible Usage**: Support for batch processing and custom workflows

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

**Option 1: Using .env file** (Recommended - Auto-loaded by the script)

```bash
# Copy the example file
cp env.example .env

# Edit and add your actual API key
nano .env
```

**Option 2: Using environment variable**

```bash
export LLAMA_CLOUD_API_KEY='your-api-key'
```

Or add it to your shell profile (`~/.zshrc` or `~/.bashrc`).

> 🔑 Get your API key from: https://developers.llamaindex.ai/python/cloud/general/api_key/

## Usage

### Basic Usage

Place your PDF file as `input.pdf` in the scripts directory and run:

```bash
python pdf_parser.py
```

### Output Files

The script generates:

- `markdown_documents.md` - Markdown version of the PDF
- `result.json` - Structured JSON with all extracted data
- `images/` - Directory containing extracted images

### Customization

Modify the configuration in the `main()` function:

```python
# Change input/output paths
pdf_path = "./your-file.pdf"
markdown_output = "./output.md"
json_output = "./data.json"
images_dir = "./extracted-images"

# Customize parser settings
config = ParserConfig(
    api_key=api_key,
    max_pages=50,  # Increase page limit
    high_res_ocr=True,  # Enable high-res OCR
)
```

## Architecture

### Project Structure

```
scripts/
├── pdf_parser.py          # Main parser implementation
├── config.py              # Configuration management
├── biology_textbook.py    # Biology textbook structure & chapter/lecture lookup
├── example_usage.py       # Usage examples
├── test_biology.py        # Test script for chapter/lecture lookup
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

### Core Modules

#### `config.py` - Configuration Management

- **`ParserSettings`**: Dataclass for parser configuration (API key, OCR settings, etc.)
- **`PathSettings`**: Dataclass for input/output file paths
- **`load_settings_from_env()`**: Load configuration from environment variables
- **`get_default_paths()`**: Get default file paths

#### `pdf_parser.py` - Main Parser

- **`PDFParser`**: Main parser class with methods for:
  - PDF parsing (text and images)
  - Markdown extraction
  - Image extraction
  - JSON result building
- **`run_parser()`**: High-level function to run complete parsing workflow
- **`main()`**: CLI entry point with error handling

#### `biology_textbook.py` - Textbook Structure

- **`BiologyTextbook`**: Dataclass containing complete textbook structure (chapters, lectures, page ranges)
- **`get_chapter_and_lecture_by_page()`**: Look up chapter and lecture for any page number
- **`get_chapter_info()`**: Get only chapter information
- **`get_lecture_info()`**: Get only lecture information
- **`BIOLOGY_TEXTBOOK`**: Pre-loaded Persian biology textbook (Grade 10) structure

#### `example_usage.py` - Usage Examples

- 8 different usage examples covering common scenarios
- Demonstrates batch processing, custom configuration, manual control, and chapter/lecture lookup

#### `test_biology.py` - Testing Script

- Test chapter and lecture detection
- Verify textbook structure
- Display all chapters and lectures

### Design Principles

- **Single Responsibility**: Each module and method has one clear purpose
- **Dependency Injection**: Configuration passed via dataclasses
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Type Hints**: Full type annotations for IDE support and error prevention
- **Documentation**: Detailed docstrings for all public functions
- **Separation of Concerns**: Configuration, parsing logic, and execution are separate
- **Testability**: Pure functions and dependency injection enable easy testing
- **Extensibility**: Easy to add new parsers or output formats

## Configuration Options

| Option                      | Default | Description                         |
| --------------------------- | ------- | ----------------------------------- |
| `max_pages`                 | 25      | Maximum number of pages to parse    |
| `high_res_ocr`              | True    | Use high-resolution OCR (slower)    |
| `adaptive_long_table`       | True    | Detect and adapt long tables        |
| `outlined_table_extraction` | True    | Extract outlined tables             |
| `output_tables_as_html`     | True    | Output tables as HTML               |
| `precise_bounding_box`      | True    | Use precise bounding box extraction |

## Error Handling

The script handles common errors:

- Missing API key
- File not found
- Parsing failures
- Invalid configuration

All errors are caught and displayed with helpful messages.

## Examples

See `example_usage.py` for complete working examples. Here are some quick snippets:

### Parse Specific Pages

```python
from pdf_parser import PDFParser
from config import ParserSettings

settings = ParserSettings(api_key=api_key, max_pages=10)
parser = PDFParser(settings)
```

### Extract Only Images

```python
image_documents = parser.extract_images(
    image_result,
    image_dir="./figures",
    include_screenshots=False,  # Skip screenshots
    include_objects=True        # Only extract object images
)
```

### Batch Processing

```python
from pdf_parser import run_parser
from config import ParserSettings, PathSettings

settings = ParserSettings(api_key=api_key)

for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    paths = PathSettings(
        input_pdf=pdf_file,
        output_markdown=f"./output/{pdf_file}.md",
        output_json=f"./output/{pdf_file}.json",
        output_images_dir=f"./output/{pdf_file}_images"
    )
    run_parser(settings, paths)
```

### Custom Configuration

```python
settings = ParserSettings(
    api_key=api_key,
    max_pages=50,
    high_res_ocr=True,
    system_prompt="Extract scientific figures and diagrams only."
)
```

### Chapter & Lecture Lookup

```python
from biology_textbook import get_chapter_and_lecture_by_page

# Look up page 18
result = get_chapter_and_lecture_by_page(18)
print(result['chapter']['title'])  # "گوارش و جذب مواد"
print(result['lecture']['title'])  # "ساختار و عملکرد لولهٔ گوارش"

# The JSON output automatically includes this info
{
  "pages": {
    "18": {
      "page": 18,
      "text": "...",
      "chapter": {
        "id": 2,
        "title": "گوارش و جذب مواد",
        "page": 17,
        "range": {"from": 17, "to": 32}
      },
      "lecture": {
        "id": 1,
        "title": "ساختار و عملکرد لولهٔ گوارش",
        "page": 18,
        "range": {"from": 18, "to": 24}
      }
    }
  }
}
```

## Troubleshooting

**API Key Error**: Ensure `LLAMA_CLOUD_API_KEY` is set in your environment

```bash
echo $LLAMA_CLOUD_API_KEY  # Should display your key
```

**File Not Found**: Check that `input.pdf` exists in the scripts directory

**Import Error**: Install dependencies

```bash
pip install llama-cloud-services
```

## License

This script is part of the bio-intelligence project.


1. parse
2. make docs 
3. make node 
4. make index  => save in vector DB
5. query => use Other way  
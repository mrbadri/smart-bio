# Project Structure

## Directory Layout

```
scripts/
│
├── 📄 Core Scripts
│   ├── pdf_parser.py          # Main parser implementation (230 lines)
│   ├── config.py              # Configuration management (77 lines)
│   └── example_usage.py       # Usage examples (192 lines)
│
├── 📋 Configuration Files
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore            # Git ignore rules
│
├── 📖 Documentation
│   ├── README.md             # Full documentation
│   ├── QUICKSTART.md         # Quick start guide
│   ├── REFACTORING_SUMMARY.md # Refactoring details
│   └── PROJECT_STRUCTURE.md  # This file
│
├── 📂 Legacy Files (preserved)
│   ├── input.pdf             # Sample input
│   ├── result.json           # Previous results
│   ├── images/               # Previous image extracts
│   └── old/                  # Old scripts backup
│
└── 🔒 Environment (gitignored)
    ├── .env                  # API keys (create from .env.example)
    └── .venv/                # Virtual environment
```

## Module Dependency Graph

```
┌─────────────────────────────────────────────┐
│           main() - CLI Entry Point          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│        load_settings_from_env()             │
│        get_default_paths()                  │
│              (config.py)                    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         run_parser(settings, paths)         │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│            PDFParser Class                  │
│  ┌───────────────────────────────────┐     │
│  │ parse_pdf()                       │     │
│  │  ├─ _create_text_parser()        │     │
│  │  └─ _create_image_parser()       │     │
│  │                                   │     │
│  │ extract_markdown()                │     │
│  │                                   │     │
│  │ extract_images()                  │     │
│  │                                   │     │
│  │ build_json_result()               │     │
│  │  └─ _extract_page_images()       │     │
│  │                                   │     │
│  │ save_json_result()                │     │
│  └───────────────────────────────────┘     │
└─────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         LlamaParse (External API)           │
│           (llama_cloud_services)            │
└─────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│  input.pdf  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│   PDFParser.parse_pdf()  │
└──────┬───────────────────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼                             ▼
┌──────────────┐           ┌──────────────────┐
│ Text Parser  │           │  Image Parser    │
│ (Agent Mode) │           │  (LLM Mode)      │
└──────┬───────┘           └────────┬─────────┘
       │                            │
       ▼                            ▼
┌──────────────┐           ┌──────────────────┐
│ text_result  │           │  image_result    │
└──────┬───────┘           └────────┬─────────┘
       │                            │
       ├──────────┬─────────────────┤
       │          │                 │
       ▼          ▼                 ▼
┌──────────┐ ┌──────────┐  ┌──────────────┐
│ Markdown │ │   JSON   │  │   Images/    │
│   .md    │ │  .json   │  │   img_*.jpg  │
└──────────┘ └──────────┘  └──────────────┘
```

## Class Architecture

### config.py

```python
@dataclass
class ParserSettings:
    """All parser configuration in one place"""
    api_key: str
    max_pages: int = 25
    high_res_ocr: bool = True
    # ... more settings

@dataclass
class PathSettings:
    """File path configuration"""
    input_pdf: str = "./input.pdf"
    output_markdown: str = "./markdown_documents.md"
    # ... more paths
```

### pdf_parser.py

```python
class PDFParser:
    """Main parser with clean interface"""
    
    def __init__(self, settings: ParserSettings):
        """Initialize with settings"""
    
    def parse_pdf(self, path: str) -> Tuple[Any, Any]:
        """Parse PDF and return results"""
    
    def extract_markdown(self, result, path: str) -> None:
        """Extract and save markdown"""
    
    def extract_images(self, result, dir: str) -> List[Any]:
        """Extract and save images"""
    
    def build_json_result(self, text, images) -> Dict:
        """Build structured JSON output"""
    
    def save_json_result(self, data: Dict, path: str) -> None:
        """Save JSON to file"""
```

## Usage Patterns

### Pattern 1: Simple CLI Usage
```bash
export LLAMA_CLOUD_API_KEY='key'
python pdf_parser.py
```

### Pattern 2: Programmatic Usage
```python
from pdf_parser import run_parser
from config import ParserSettings, PathSettings

settings = ParserSettings(api_key='key')
paths = PathSettings(input_pdf='file.pdf')
run_parser(settings, paths)
```

### Pattern 3: Manual Control
```python
from pdf_parser import PDFParser
from config import ParserSettings

parser = PDFParser(ParserSettings(api_key='key'))
text_result, image_result = parser.parse_pdf('file.pdf')
# ... custom processing
```

### Pattern 4: Batch Processing
```python
settings = ParserSettings(api_key='key')
for pdf in pdf_files:
    paths = PathSettings(input_pdf=pdf)
    run_parser(settings, paths)
```

## Testing Strategy

```
Unit Tests (Recommended):
├── test_config.py
│   ├── test_parser_settings_defaults
│   ├── test_path_settings_defaults
│   └── test_load_settings_from_env
│
├── test_pdf_parser.py
│   ├── test_pdf_parser_init
│   ├── test_create_parsers
│   ├── test_extract_markdown
│   ├── test_extract_images
│   ├── test_build_json_result
│   └── test_extract_page_images
│
└── test_integration.py
    └── test_full_parsing_workflow
```

## Extension Points

Want to extend functionality? Here's how:

### Add New Output Format
```python
class PDFParser:
    def extract_html(self, text_result, output_path: str) -> None:
        """New method for HTML output"""
        # Implementation
```

### Add New Parser Mode
```python
def _create_custom_parser(self) -> LlamaParse:
    """Custom parser configuration"""
    return LlamaParse(
        api_key=self.settings.api_key,
        # ... custom settings
    )
```

### Add Post-Processing
```python
def post_process_text(self, text: str) -> str:
    """Post-process extracted text"""
    # Clean up, format, etc.
    return processed_text
```

## Performance Characteristics

| Operation | Time (avg) | Notes |
|-----------|------------|-------|
| Text parsing (25 pages) | 30-60s | Depends on OCR quality |
| Image extraction | 20-40s | Varies by image count |
| Markdown generation | <1s | Fast local operation |
| JSON building | <1s | Fast local operation |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLAMA_CLOUD_API_KEY` | Yes | None | API key for LlamaParse |
| `MAX_PAGES` | No | 25 | Maximum pages to parse |
| `HIGH_RES_OCR` | No | true | Enable high-res OCR |

## Security Notes

✅ **Good Practices**:
- API key stored in environment variable
- No credentials in source code
- `.env` files in `.gitignore`

⚠️ **Important**:
- Never commit `.env` file
- Never share API keys
- Use separate keys for dev/prod

## Migration from Old Code

| Old Code | New Code | Change |
|----------|----------|--------|
| Hardcoded API key | Environment variable | Security ✅ |
| Single file | 3 modules | Organization ✅ |
| No types | Full type hints | Safety ✅ |
| No docs | Comprehensive docs | Usability ✅ |
| Procedural | Object-oriented | Maintainability ✅ |

---

**Last Updated**: November 25, 2025
**Version**: 2.0 (Refactored)


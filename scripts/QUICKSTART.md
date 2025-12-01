# Quick Start Guide

Get started with the PDF Parser in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set API Key

### Option 1: Using .env file (Recommended)

```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

Then add your key to the `.env` file:

```
LLAMA_CLOUD_API_KEY=your-actual-api-key-here
```

> 💡 **Get your API key**: https://developers.llamaindex.ai/python/cloud/general/api_key/

### Option 2: Using environment variable

```bash
export LLAMA_CLOUD_API_KEY='your-api-key-here'
```

**Make it permanent** by adding to your shell profile:

```bash
# For zsh (macOS default)
echo 'export LLAMA_CLOUD_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export LLAMA_CLOUD_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Step 3: Run the Parser

```bash
python pdf_parser.py
```

That's it! 🎉

## What Happens

The parser will:

1. ✅ Parse `input.pdf` in the current directory
2. ✅ Extract text and convert to markdown → `markdown_documents.md`
3. ✅ Extract images → `images/` directory
4. ✅ Generate structured JSON → `result.json`

## Example Output

```
============================================================
PDF Parser using LlamaParse
============================================================

📄 Parsing PDF: ./input.pdf
  ⏳ Extracting text content...
  ⏳ Extracting images...
  ✓ PDF parsed successfully
📝 Extracting markdown...
  ✓ Saved: ./markdown_documents.md
🖼️  Extracting images...
  ✓ Extracted 12 images to: ./images
🔧 Building JSON result...
  ✓ Processed 25 pages
💾 Saving JSON result...
  ✓ Saved: ./result.json

============================================================
✓ All tasks completed successfully!
============================================================
```

## Next Steps

### Custom Input File

```bash
# Edit the main() function in pdf_parser.py
# Change: pdf_path = "./input.pdf"
# To: pdf_path = "./your-file.pdf"
```

### Process Multiple PDFs

```bash
# Use the batch processing example
python example_usage.py
# (Uncomment example_batch_processing in the file)
```

### Custom Configuration

```python
from pdf_parser import run_parser
from config import ParserSettings, PathSettings

# Your custom settings
settings = ParserSettings(
    api_key="your-key",
    max_pages=10  # Process only first 10 pages
)

paths = PathSettings(
    input_pdf="./my-document.pdf",
    output_markdown="./output.md"
)

run_parser(settings, paths)
```

## Common Issues

### Issue: "LLAMA_CLOUD_API_KEY not found"

**Solution**: You have two options:

1. **Using .env file** (Recommended):

```bash
# Create .env file from example
cp env.example .env

# Edit and add your key
nano .env
```

2. **Using environment variable**:

```bash
export LLAMA_CLOUD_API_KEY='your-key'
echo $LLAMA_CLOUD_API_KEY  # Verify it's set
```

**Note**: The script automatically loads `.env` files, so you don't need to export manually if you use a `.env` file!

### Issue: "PDF file not found: ./input.pdf"

**Solution**: Either:

1. Add a file named `input.pdf` to the scripts directory, or
2. Change the `pdf_path` in the script to point to your PDF

### Issue: "Import llama_cloud_services could not be resolved"

**Solution**: Install the package:

```bash
pip install llama-cloud-services
```

### Issue: "Permission denied" when running script

**Solution**: Make sure the script is executable:

```bash
chmod +x pdf_parser.py
```

## Performance Tips

### Fast Mode (Lower Quality, Faster)

```python
settings = ParserSettings(
    api_key=api_key,
    high_res_ocr=False  # Disable high-res OCR
)
```

### Process Fewer Pages

```python
settings = ParserSettings(
    api_key=api_key,
    max_pages=5  # Only first 5 pages
)
```

### Skip Image Extraction

```python
# In pdf_parser.py, comment out:
# image_documents = parser.extract_images(image_result, paths.output_images_dir)
```

## Documentation

- **Full Documentation**: See `README.md`
- **Usage Examples**: See `example_usage.py`
- **Refactoring Details**: See `REFACTORING_SUMMARY.md`

## Support

For issues or questions:

1. Check the `README.md` for detailed information
2. Review `example_usage.py` for code examples
3. Check the LlamaParse documentation: https://docs.llamaindex.ai/

---

**Happy Parsing! 🚀**

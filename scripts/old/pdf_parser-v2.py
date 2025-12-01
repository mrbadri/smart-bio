# DOLING ---- - --- - --- -
# docling_fix.py
# pip install -U docling
# (mac) brew install tesseract
# (linux) sudo apt-get install tesseract-ocr tesseract-ocr-fas

from pathlib import Path
import json

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling.document_converter import DocumentConverter, PdfFormatOption
from rtl_fix import fix_rtl_text

pdf_path = Path("input.pdf")
out_dir = Path("out")
out_dir.mkdir(exist_ok=True)

# 1) OCR دستی با tesseract (فارسی)
ocr_opts = TesseractCliOcrOptions()
ocr_opts.lang = ["fas"]   # اگر زبان‌پک auto داری می‌تونی ["auto"] بزاری

pipeline_opts = PdfPipelineOptions()
pipeline_opts.do_ocr = True
pipeline_opts.ocr_options = ocr_opts

# 2) سنگینی layout/table رو کم کن (اختیاری ولی برای رفع هنگ مفید)
pipeline_opts.do_table_structure = False

# 3) اجباراً CPU تا وارد MPS/ocrmac نشه
pipeline_opts.accelerator_options = AcceleratorOptions(
    device=AcceleratorDevice.CPU, num_threads=4
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_opts)
    }
)

result = converter.convert(pdf_path)
doc = result.document

md = doc.export_to_markdown()
md_fixed = fix_rtl_text(md)

(out_dir / "doc.md").write_text(md_fixed, encoding="utf-8")
(out_dir / "doc.json").write_text(
    json.dumps(doc.export_to_dict(), ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("PDF parsed successfully -> out/doc.md , out/doc.json")

# llx-XBtyThevmRXlr43daJL7KZkax3NRFKvLl8BC5LXTTaHIaSln
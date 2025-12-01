
# pip install -U PyPDF2

# from pathlib import Path
# import json
# import re
# from PyPDF2 import PdfReader  # در نسخه‌های جدید: PdfReader

# pdf_path = Path("input.pdf")
# out_dir = Path("out")
# out_dir.mkdir(exist_ok=True)

# # ---------------------------
# # RTL fix (برعکس شدن کلمات)
# # ---------------------------
# ARABIC_CHARS = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
# LTR_SPAN = re.compile(
#     r'(https?://\S+|[\w.+-]+@[\w-]+\.[\w.-]+|[A-Za-z0-9][A-Za-z0-9._:/\-]*)'
# )

# def is_rtl_line(line: str) -> bool:
#     rtl = len(ARABIC_CHARS.findall(line))
#     ltr = len(re.findall(r'[A-Za-z]', line))
#     return rtl > ltr * 2  # heuristic

# def fix_rtl_line(line: str) -> str:
#     ltr_parts = []
#     def repl(m):
#         ltr_parts.append(m.group(0))
#         return f"@@LTR{len(ltr_parts)-1}@@"

#     temp = LTR_SPAN.sub(repl, line)
#     tokens = temp.split()
#     tokens.reverse()
#     temp2 = " ".join(tokens)

#     for i, part in enumerate(ltr_parts):
#         temp2 = temp2.replace(f"@@LTR{i}@@", part)
#     return temp2

# def fix_rtl_text(text: str) -> str:
#     out_lines = []
#     for ln in text.splitlines():
#         # هدرهای markdown، لیست‌ها، کد بلاک… را دست نزن
#         if ln.strip().startswith(("#", "```", "-", "*", ">")) or not ln.strip():
#             out_lines.append(ln)
#             continue

#         if is_rtl_line(ln):
#             out_lines.append(fix_rtl_line(ln))
#         else:
#             out_lines.append(ln)
#     return "\n".join(out_lines)

# # ---------------------------
# # PDF text extraction
# # ---------------------------

# reader = PdfReader(str(pdf_path))
# pages_out = []
# md_parts = []

# for i, page in enumerate(reader.pages, start=1):
#     raw = page.extract_text() or ""  # API اصلی استخراج متن  [oai_citation:1‡pypdf2.readthedocs.io](https://pypdf2.readthedocs.io/en/3.x/user/extract-text.html?utm_source=chatgpt.com)

#     # پاکسازی کاراکترهای کنترلی عجیب (مثل همان Backspaceها که تو نمونه‌ات بود)
#     raw = raw.replace("\x08", " ")
#     raw = re.sub(r"[ \t]+", " ", raw)
#     raw = re.sub(r"\n{3,}", "\n\n", raw).strip()

#     fixed = fix_rtl_text(raw)

#     pages_out.append({
#         "page": i,
#         "text": fixed
#     })

#     md_parts.append(f"## صفحه {i}\n\n{fixed}\n")

# md_text = "\n".join(md_parts)

# (out_dir / "doc.md").write_text(md_text, encoding="utf-8")
# (out_dir / "doc.json").write_text(
#     json.dumps({"pages": pages_out}, ensure_ascii=False, indent=2),
#     encoding="utf-8"
# )

# print("PDF parsed successfully -> out/doc.md , out/doc.json")















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

(out_dir / "doc.md").write_text(doc.export_to_markdown(), encoding="utf-8")
(out_dir / "doc.json").write_text(
    json.dumps(doc.export_to_dict(), ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("PDF parsed successfully -> out/doc.md , out/doc.json")
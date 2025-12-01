import json
from pathlib import Path

from llama_index.core import Document
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,
    SentenceWindowNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from config import load_openai_settings

# --- تنظیمات اولیه مسیرها ---
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

# --- 1) Load OpenAI config ---
openai_config = load_openai_settings()

embed_model = OpenAIEmbedding(
    model=openai_config.embedding_model,
    api_key=openai_config.api_key,
)

# --- 2) تعریف پارسرها ---

# پارسر معنایی (چانک‌های بزرگ‌تر، topic-level)
semantic_parser = SemanticSplitterNodeParser(
    embed_model=embed_model,
    breakpoint_threshold_type="percentile",   # یا "standard_deviation"
    breakpoint_threshold_amount=0.95,         # هرچی پایین‌تر، چانک‌های ریزتر
)

# پارسر جمله + پنجره (sentence window)
sentence_window_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,                       # چند جمله قبل/بعد را در window نگه دارد
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)

# --- 3) خواندن docs از out/docs.json ---
with open(OUT_DIR / "nodes.json", "r", encoding="utf-8") as f:
    docs_json = json.load(f)

docs = [
    Document(text=doc["text"], metadata=doc["metadata"])
    for doc in docs_json
]

# --- 4) ساخت نودهای معنایی ---
semantic_nodes = semantic_parser.get_nodes_from_documents(docs)

semantic_nodes_json = [
    {
        "text": node.text,
        "metadata": node.metadata,
        "node_id": node.node_id,
        "start_char_idx": node.start_char_idx,
        "end_char_idx": node.end_char_idx,
        "parser_type": "semantic",
    }
    for node in semantic_nodes
]

with open(OUT_DIR / "semantic_nodes.json", "w", encoding="utf-8") as f:
    json.dump(semantic_nodes_json, f, ensure_ascii=False, indent=2)

# --- 5) ساخت نودهای sentence window ---
sentence_nodes = sentence_window_parser.get_nodes_from_documents(docs)

sentence_nodes_json = [
    {
        "text": node.text,                 # جمله اصلی
        "metadata": node.metadata,         # شامل "window" و "original_text"
        "node_id": node.node_id,
        "start_char_idx": node.start_char_idx,
        "end_char_idx": node.end_char_idx,
        "parser_type": "sentence_window",
    }
    for node in sentence_nodes
]

with open(OUT_DIR / "sentence_window_nodes.json", "w", encoding="utf-8") as f:
    json.dump(sentence_nodes_json, f, ensure_ascii=False, indent=2)

print("✅ semantic_nodes.json and sentence_window_nodes.json created successfully.")
import json
from pathlib import Path

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.schema import TextNode
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from config import load_openai_settings

BASE_DIR = Path(__file__).parent
OUT_DIR = BASE_DIR / "out"
STORAGE_DIR = BASE_DIR / "out/semantic_index"
STORAGE_DIR.mkdir(exist_ok=True)

# 1) Load config
openai_config = load_openai_settings()

Settings.llm = OpenAI(
    model=openai_config.chat_model,   # مثلاً gpt-4.1-mini
    api_key=openai_config.api_key,
)

Settings.embed_model = OpenAIEmbedding(
    model=openai_config.embedding_model,  # مثلاً text-embedding-3-small
    api_key=openai_config.api_key,
)

# 2) Load semantic_nodes.json
with open(OUT_DIR / "semantic_nodes.json", "r", encoding="utf-8") as f:
    nodes_json = json.load(f)

nodes = []
for item in nodes_json:
    node = TextNode(
        text=item["text"],
        id_=item["node_id"],
        metadata=item.get("metadata") or {},
        start_char_idx=item.get("start_char_idx"),
        end_char_idx=item.get("end_char_idx"),
    )
    nodes.append(node)

# 3) ساخت Index
index = VectorStoreIndex(nodes)

# 4) ذخیره برای استفاده بعدی
index.storage_context.persist(persist_dir=str(STORAGE_DIR))

print("✅ semantic index for bio10 created and stored in", STORAGE_DIR)
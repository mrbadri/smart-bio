from pathlib import Path

from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from config import load_openai_settings

BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / "out/semantic_index"

openai_config = load_openai_settings()

Settings.llm = OpenAI(
    model=openai_config.chat_model,
    api_key=openai_config.api_key,
)

Settings.embed_model = OpenAIEmbedding(
    model=openai_config.embedding_model,
    api_key=openai_config.api_key,
)

# 1) Load existing index
storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
index = load_index_from_storage(storage_context=storage_context)

# 2) Create query engine with custom prompt
SYSTEM_PROMPT = """
شما یک معلم زیست‌شناسی دبیرستان هستید.
فقط و فقط بر اساس متن‌های کتاب زیست (دهم فعلاً) پاسخ بده.
اگر جواب در منبع وجود نداشت، صریح بگو «در منابع موجود پیدا نکردم».
پاسخ را به زبان فارسی ساده و سطح دانش‌آموز دبیرستان بده.
اگر لازم بود، حتماً صفحه/فصل را هم ذکر کن (اگر در متادیتا موجود است).
"""

response_mode = "compact"

qa_prompt_tmpl = PromptTemplate(
    "Student's question:\n{query_str}\n\n"
    "Answer based on the following sections from the book:\n"
    "{context_str}\n\n"
    "Final answer (in simple Persian):"
)

query_engine = index.as_query_engine(
    similarity_top_k=5,
    text_qa_template=qa_prompt_tmpl,
    response_mode=response_mode,
)

if __name__ == "__main__":
    while True:
        q = input("\n❓ Your question about biology (exit to quit): ")
        if q.strip().lower() in ["exit", "quit"]:
            break

        resp = query_engine.query(q)
        print("\n🧠 Answer:\n", resp)
        # If you want to also print the sources:
        print("\n📚 Sources used:")
        for src in resp.source_nodes:
            meta = src.metadata or {}
            print(
                f"- page={meta.get('page')}, "
                f"chapter={meta.get('chapter_title')}, "
                f"score={src.score:.3f}"
            )
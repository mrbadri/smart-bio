import json
from llama_index.core import Document

with open("out/output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

docs = []

for page_key, page_obj in data["pages"].items():
    md = page_obj["md"]
    chapter = page_obj.get("chapter") or {}
    lecture = page_obj.get("lecture") or {}

    metadata = {
        "book": "biology-textbook",
        "grade": 10,
        "page": page_obj["page"],
        "chapter_id": chapter.get("id"),
        "chapter_title": chapter.get("title"),
        "chapter_from": chapter.get("range", {}).get("from"),
        "chapter_to": chapter.get("range", {}).get("to"),
        "lecture_id": lecture.get("id"),
        "lecture_title": lecture.get("title"),
        "lecture_from": lecture.get("range", {}).get("from"),
        "lecture_to": lecture.get("range", {}).get("to"),
    }

    doc = Document(text=md, metadata=metadata)
    # Convert Document to dict for JSON serialization
    docs.append({
        "text": doc.text,
        "metadata": doc.metadata,
        "doc_id": doc.doc_id
    })
    
    
    
#  write docs in out/docs.json
with open("out/nodes.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
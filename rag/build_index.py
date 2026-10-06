import os
import json

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from rag import load_document, split_text

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)

text = load_document(
    "knowledge/company_policy.txt"
)

chunks = split_text(
    text,
    "company_policy.txt"
)

embeddings = np.array([
    chunk["embedding"]
    for chunk in chunks
]).astype(np.float32)

print(
    "embedding shape:",
    embeddings.shape
)

faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
faiss_index.add(embeddings)

print(
    "FAISS数量:",
    faiss_index.ntotal
)

os.makedirs("index", exist_ok=True)
faiss.write_index(faiss_index, "index/faiss_index")

metadata = [
    {
        "content": chunk["content"],
        "source": chunk["source"],
    }
    for chunk in chunks
]

with open("index/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)


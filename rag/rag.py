from pathlib import Path
from sentence_transformers import SentenceTransformer

import utils

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)


def load_document(path):
    text = Path(path).read_text(encoding="utf-8")
    return text


def split_text(text, source):
    chunks = text.split("\n\n")

    return [
        {
            "content": chunk.strip(),
            "source": source,
            "embedding":model.encode(chunk.strip())
        }
        for chunk in chunks
        if chunk.strip()
    ]

def split_text_new(text, source):
    chunks = text.split("\n\n")

    return [
        {
            "content": chunk.strip(),
            "source": source,
        }
        for chunk in chunks
        if chunk.strip()
    ]

def split_text_opt(text, chunk_size, overlap, source):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return [
        {
            "content": chunk.strip(),
            "source": source,
        }
        for chunk in chunks
        if chunk.strip()
    ]


def search(keywords, chunks):
    results = []
    for chunk in chunks:
        for keyword in keywords:
            if keyword in chunk["content"]:
                results.append(chunk)
                break
    return results


def vector_search(query_vector, chunks, top_k):
    results = []
    for chunk in chunks:
        score = utils.cosine_similarity(query_vector, chunk["embedding"])
        results.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "score": score
        })
        results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def build_prompt(context, question):
    prompt = f"""
    请根据以下资料回答问题。
    资料：{context}
    问题：{question}
    要求：
    1. 只根据资料回答
    2. 如果资料没有答案，请说不知道
    """
    return prompt

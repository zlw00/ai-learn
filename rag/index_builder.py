from pathlib import Path
from sentence_transformers import SentenceTransformer
import rag
import faiss
import numpy as np
import json

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)
def build_index(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    chunks = rag.split_text_opt(
        text,10,5,
        Path(file_path).name
    )
    embeddings = np.array(
        [
            model.encode(
                chunk["content"]
            )
            for chunk in chunks
        ]
    ).astype("float32")

    # embeddings = np.array([
    #     chunk["embedding"]
    #     for chunk in chunks
    # ]).astype(np.float32)

    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)

    Path("index").mkdir(
        exist_ok=True
    )
    faiss.write_index(
        faiss_index,
        "index/faiss_index"
    )

    metadata = [
        {
            "content": chunk["content"],
            "source": chunk["source"],
        }
        for chunk in chunks
    ]

    with open(
            "index/metadata.json",
            "w",
            encoding="utf-8"
    ) as f:
        json.dump(
            metadata,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        "知识库构建完成"
    )



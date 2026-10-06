import json
import faiss
import numpy as np


class Retriever:
    def __init__(self, model, index_path, metadata_path):
        self.model = model
        self.index = faiss.read_index(
            index_path
        )
        with open(
            metadata_path,
            encoding="utf-8"
        ) as f:
            self.metadata = json.load(f)


    def search(self, question, top_k):
        question_vector = self.model.encode(question)
        question_vector = np.array(
            [question_vector]
        ).astype(np.float32)

        distances, indices = self.index.search(question_vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append(
                {
                    "content":self.metadata[idx]["content"],
                    "source":self.metadata[idx]["source"],
                    "score":float(dist),
                }
            )
        return results



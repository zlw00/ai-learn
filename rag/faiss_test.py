import numpy as np
import faiss


dimension = 3


def create_index(dimension):
    index = faiss.IndexFlatL2(dimension)
    return index


index = create_index(
    dimension
)

vectors = np.array(
    [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
).astype("float32")


index.add(vectors)


print(
    "向量数量:",
    index.ntotal
)
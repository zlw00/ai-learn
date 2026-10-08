from bm25_retriever import Bm25Retriever
from retriever import Retriever
from sentence_transformers import SentenceTransformer
from reranker import Reranker


class HybridRetriever:
    def __init__(self, bm25_retriever, vector_retriever):
        self.bm25_retriever = bm25_retriever
        self.vector_retriever = vector_retriever

    def search(self, question, top_k=3):
        keywords_results = self.bm25_retriever.keyword_search(question, top_k)
        vector_results = self.vector_retriever.search(question, top_k)
        return self.fuse_results(keywords_results, vector_results)

    def fuse_results(self, keywords_results, vector_results):
        k = 60
        scores = {}
        contents = {}
        for rank, result in enumerate(keywords_results):
            content = result["content"]
            scores[content] = scores.get(content, 0) + 1 / (k + rank + 1)
            contents[content] = result
        for rank, result in enumerate(vector_results):
            content = result["content"]
            scores[content] = scores.get(content, 0) + 1 / (k + rank + 1)
            contents[content] = result
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        results = []
        for content, score in sorted_scores:
            result_content = contents[content].copy()
            result_content["score"] = score
            results.append(result_content)
        return results


if __name__ == '__main__':
    model = SentenceTransformer(
        "BAAI/bge-small-zh-v1.5"
    )
    index_path = "index/faiss_index"
    metadata_path = "index/metadata.json"
    vector_retriever = Retriever(model, index_path, metadata_path)
    bm25_retriever = Bm25Retriever(vector_retriever.metadata)
    hybridRetriever = HybridRetriever(bm25_retriever, vector_retriever)
    question = "几点打卡"
    #没有融合前的结果分别输出
    # keywords_results, vector_results = hybridRetriever.search(question, 3)
    # print("===== BM25 =====")
    # for result in keywords_results:
    #     print(result)
    #
    # print("===== Vector =====")
    # for result in vector_results:
    #     print(result)

    # 融合后的结果输出
    results = hybridRetriever.search(question)
    reranker = Reranker()
    results = reranker.reranker(question, results,top_k=2)
    for result in results:
        print(result)

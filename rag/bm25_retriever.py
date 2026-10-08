from rank_bm25 import BM25Okapi
import jieba

class Bm25Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        documents = [
            chunk["content"]
            for chunk in self.chunks
        ]
        tokenized_documents = [
            list(jieba.cut(document)) #中文分词
            for document in documents
        ]
        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def keyword_search(self, question, top_k=3):
        query_tokens = list(jieba.cut(question))
        scores = self.bm25.get_scores(
            query_tokens
        )
        top_indices = scores.argsort()[
            ::-1
        ][:top_k]

        results = []
        for index in top_indices:
            results.append(
                {
                    "content": self.chunks[index]["content"],
                    "source": self.chunks[index]["source"],
                    "score": float(scores[index])
                }
            )

        return results

if __name__ == '__main__':
    chunks = [
        {
            "content": "HTTP 401表示身份认证失败",
            "source": "test.txt"
        },
        {
            "content": "HTTP 500表示服务器内部错误",
            "source": "test.txt"
        },
        {
            "content": "年假需要提前3个工作日申请",
            "source": "company_policy.txt"
        }
    ]
    hybridRetriever = Bm25Retriever(chunks)
    question = "HTTP 401"
    results = hybridRetriever.keyword_search(question, 3)
    for result in results:
        print(result)


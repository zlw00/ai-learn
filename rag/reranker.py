import jieba

class Reranker:
    def reranker(self, question, results, top_k=3):
        for result in results:
            content = result["content"]
            score = self.calculate_score(
                question,
                content
            )
            result["rerank_score"] = score

        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]

    def calculate_score(self, question, content):
        question_words = set(jieba.cut(question))
        content_words = set(jieba.cut(content))
        common_words = question_words & content_words
        return len(common_words)


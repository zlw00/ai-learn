from services.memory import ChatMemory
from services.query_rewriter import QueryRewriter


class RagService:
    def __init__(self, retriever, generator, client):
        self.retriever = retriever
        self.generator = generator
        self.memory = ChatMemory()
        self.query_rewriter = QueryRewriter(
            client
        )

    def chat(self, session_id, question):
        history = self.memory.get_history(session_id)
        rewrite_question = self.query_rewriter.rewrite(history, question)
        results = self.retriever.search(rewrite_question, 3)
        ans = self.generator.generate_ans(rewrite_question, results)
        self.memory.add_message(
            session_id,
            "user",
            rewrite_question
        )
        self.memory.add_message(
            session_id,
            "assistant",
            ans
        )
        # sources = list(
        #     set(
        #         item["source"]
        #         for item in results
        #     )
        # )
        references = [
            {
                "source": item["source"],
                "content": item["content"]
            }
            for item in results
        ]
        return {
            "answer": ans,
            "references": references,
            "history": history,
            "rewrite_question": rewrite_question
        }


    def chat_stream(
            self,
            session_id,
            question
    ):
        history = self.memory.get_history(
            session_id
        )

        rewrite_question = self.query_rewriter.rewrite(
            history,
            question
        )

        results = self.retriever.search(
            rewrite_question,
            3
        )

        for token in self.generator.generate_stream(
                question,
                results
        ):
            yield f"data:{token}\n\n"


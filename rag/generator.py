import rag


class Generator:

    def __index__(self, model, client):
        self.model = model
        self.client = client


    def generate_answer(
        self,
        question,
        results
    ):
        context = "\n".join(
            [
                item["content"]
                for item in results
            ]
        )
        prompt = rag.build_prompt(
            context,
            question
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content





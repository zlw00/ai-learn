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


class Generator:
    def __init__(self, model, client):
        self.model = model
        self.client = client

    def generate_ans(self, question, results):
        if not results:
            return "知识库中没有找到相关信息"

        context = "\n".join([
            result["content"]
            for result in results
        ])
        prompt = build_prompt(context, question)

        response = self.client.chat.completions.create(
            model = self.model,
            messages = [{
                "role":"user",
                "content":prompt

            }]
        )
        return response.choices[0].message.content

    def generate_stream(self, question, results):
        if not results:
            return "知识库中没有找到相关信息"

        context = "\n".join([
            result["content"]
            for result in results
        ])
        prompt = build_prompt(context, question)

        response = self.client.chat.completions.create(
            model = self.model,
            messages = [{
                "role":"user",
                "content":prompt

            }],
            stream = True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content #return是一次性返回，而yield是一点一点返回






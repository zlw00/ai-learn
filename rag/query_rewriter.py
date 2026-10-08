class QueryRewriter:

    def __init__(self, client, model):
        self.client = client
        self.model = model


    def rewrite(self, history, question):

        prompt = f"""
            你是一个问题改写助手。

            根据历史对话，把用户当前问题改写成一个完整的问题。

            历史对话：
            {history}

            当前问题：
            {question}

            要求：
            1. 保留原问题含义
            2. 如果当前问题已经完整，不需要修改
            3. 只输出改写后的问题
            """

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
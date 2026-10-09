
class QueryRewriter:
    def __init__(self, client):
        self.client = client


    def rewrite(self, history, question):

        if not history:
            return question

        prompt = f"""
        你是一个搜索问题优化助手。

        根据历史对话，将用户当前问题改写成一个完整的问题。

        要求：
        1. 不回答问题
        2. 只输出改写后的问题
        3. 保留原问题含义


        历史对话:
        {history}


        当前问题:
        {question}


        改写后的问题:
        """
        response = self.client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()
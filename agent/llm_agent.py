import json

from zhipuai import ZhipuAI
from dotenv import load_dotenv

from tools import (
    search_knowledge,
    get_time
)

import os

from tools_schema import tools


class Agent:


    def __init__(
        self,
        client
    ):
        self.client = client


    def run(
        self,
        question
    ):

        response = self.client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role":"system",
                    "content":
                        f"""
                        你必须作为Agent运行。
                        
                        规则：
                        
                        1. 如果问题涉及公司制度、假期、流程，必须调用 search_knowledge。
                        
                        2. 调用工具时，只允许输出JSON。
                        
                        3. 禁止输出解释文字。
                        可以使用的工具：{tools}
                        
                        JSON格式必须严格如下：
                        {{
                         "tool":"search_knowledge",
                         "input":"用户问题"
                        }}
                        
                        不要输出markdown。
                        不要输出代码块。
                        不要输出其他内容。
                        """
                },
                {
                    "role":"user",
                    "content":question
                }
            ]
        )


        content = response.choices[0].message.content


        return self.execute(
            content
        )

    def execute(
        self,
        content
    ):

        try:
            action = json.loads(
                content
            )
        except:
            return content

        tool = action["tool"]

        input = action.get(
            "input"
        )

        if tool == "search_knowledge":
            return search_knowledge(
                input
            )

        if tool == "get_time":
            return get_time()

        return "未知工具"

if __name__ == "__main__":
    load_dotenv()
    client = ZhipuAI(
        api_key=os.getenv(
            "ZHIPU_API_KEY"
        )
    )
    agent = Agent(client)


    question = "病假需要多久申请"

    answer = agent.run(
        question
    )

    print(answer)
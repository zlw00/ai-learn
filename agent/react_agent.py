import json

from dotenv import load_dotenv
from zhipuai import ZhipuAI
import os


class ReActAgent:
    def __init__(self, client):
        self.client = client

    def run(self, question):
        messages = [
            {
                "role": "system",
                "content":
                    """
你是企业知识库Agent。
    
你拥有以下工具：

search_knowledge:
查询企业知识库。

calculator：
数学计算

get_time：
获取当前时间


规则：

1.
任何关于公司制度、假期、流程的问题，
必须调用search_knowledge。


2.
禁止使用自己的知识回答企业制度问题。


3.
调用工具必须只返回JSON。


格式：

{
 "action":工具名称,
 "input":"问题"
}

"""
            },
            {
                "role": "user",
                "content": question
            }
        ]

        while True:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=messages
            )
            content = response.choices[0].message.content
            print("content:" + content)

            # 判断是否调用工具
            try:
                action = json.loads(
                    content
                )
            except:
                # 最终答案
                return content

            tool_name = action.get(
                "action"
            )

            tool_input = action.get(
                "input"
            )
            from tools import search_knowledge, get_time, calculator
            if tool_name == "search_knowledge":
                observation = search_knowledge(
                    tool_input
                )
                print("observation" + observation)
            elif tool_name == "get_time":
                observation = get_time()
            elif tool_name == "calculator":
                observation = calculator(tool_input)
            else:

                observation = "没有找到工具"

                # 把工具结果加入上下文

            messages.append(
                {
                    "role": "assistant",
                    "content": content
                }
            )

            messages.append(
                {
                    "role": "user",
                    "content":
                        f"""
                        工具执行结果：
                        {observation}
                        请根据工具结果回答用户。
                        """
                }
            )


if __name__ == '__main__':
    load_dotenv()

    client = ZhipuAI(
        api_key=os.getenv(
            "ZHIPU_API_KEY"
        )
    )

    agent = ReActAgent(
        client
    )

    answer = agent.run(
        "获取当前时间"
    )

    print(answer)

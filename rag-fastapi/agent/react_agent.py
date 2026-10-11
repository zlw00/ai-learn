import json

from dotenv import load_dotenv
from zhipuai import ZhipuAI
import os
from sentence_transformers import SentenceTransformer
from services.retriever import Retriever
from services.generator import Generator
from services.rag_service import RagService

from agent.tools import rag_tool,tools_fun,function_schema

class ReActAgent:
    def __init__(self, client):
        self.client = client

    def run(self, question):
        global tool_call
        messages = [
            {
                "role": "system",
                "content":
                    """
                    你是企业知识库Agent。
            
                    任何公司制度问题必须调用search_knowledge
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
                messages=messages,
                tools=function_schema.tools   #使用Function Calling
            )
            message = response.choices[0].message
            print(message)
            print("content:" + message.content)

            if message.tool_calls:
                tool_call = message.tool_calls[0]
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name == "search_knowledge":
                    observation = tools_fun.search_knowledge(
                        arguments["query"]
                    )
                    # print("observation" + observation)
                elif tool_name == "get_time":
                    observation =tools_fun.get_time()
                elif tool_name == "calculator":
                    observation = tools_fun.calculator(arguments["query"])
                else:
                    observation = "没有找到工具"

                messages.append(message.model_dump())  #把 Pydantic 对象，转换成普通 Python 字典 dict。
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id":tool_call.id,
                        "content":str(observation)
                    }
                )
            else:
                return message.content


if __name__ == '__main__':
    load_dotenv()
    client = ZhipuAI(
        api_key=os.getenv(
            "ZHIPU_API_KEY"
        )
    )

    index_path = "../index/faiss_index"
    metadata_path = "../index/metadata.json"
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")  # Embedding 向量模型
    retriever = Retriever(model, index_path, metadata_path)
    generator = Generator("glm-4-flash", client)

    rag_service = RagService(retriever, generator, client)
    rag_tool = rag_tool.RagTool(rag_service)
    tools_fun.init_tools(rag_tool)
    agent = ReActAgent(client)
    answer = agent.run("病假呢")
    print(answer)

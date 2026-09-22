#
# from google import genai
# from dotenv import load_dotenv
# import os
#
# # 加载.env里面的环境变量
# load_dotenv()
#
# # 读取key，没有硬编码写进代码！
# api_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)
#
# def ask_ai(question: str):
#     response = client.models.generate_content(
#         model="gemini-2.5-flash", # 免费可用模型
#         contents=question
#     )
#     return response.text
#
#
# if __name__ == "__main__":
#     print("==== AI Chat CLI (Gemini) ====")
#     user_input = input("请输入你的问题：")
#     answer = ask_ai(user_input)
#     print("\nAI回答：")
#     print(answer)


from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os

# 加载.env里面的环境变量
load_dotenv()

# 从环境变量读取key，key没有硬编码写在代码里！
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)

def ask_ai(question: str):
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("==== AI Chat CLI ====")
    user_input = input("请输入你的问题：")
    answer = ask_ai(user_input)
    print("\nAI回答：")
    print(answer)

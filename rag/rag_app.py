from rag import load_document, build_prompt, split_text, search, vector_search
from dotenv import load_dotenv
import os
from zhipuai import ZhipuAI
from sentence_transformers import SentenceTransformer


load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)

text = load_document(
    "knowledge/company_policy.txt"
)

# print(f"text:{text}")
chunks = split_text(text,"company_policy.txt")

question = "年假需要提前多久申请"
'''
    embedding计算
'''
model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)
query_vector = model.encode(question)

results = vector_search(query_vector, chunks, 3)


'''
    关键词检索
'''
# keywords = ["年假","申请"]
# results = search(keywords, chunks)

context = "\n\n".join([f"来源:{item['source']}\n内容:{item['content']}" for item in results])

prompt = build_prompt(context, question)
# print(f"prompt:{prompt}")

msg = [
    {
        "role": "user",
        "content": prompt
    }
]

response = client.chat.completions.create(
    model=MODEL,
    messages=msg
)
print(f"AI回答：{response.choices[0].message.content}")

# sources = set(
#     item["source"]
#     for item in results
# )

# for source in sources:
#     print(
#         f"来源:{source}"
#     )

for result in results:
    print(
        f"来源：{result['source']}, 分数：{result['score']}"
    )
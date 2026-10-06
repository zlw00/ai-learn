import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

import rag

index = faiss.read_index(
    "index/faiss_index"
)

print(
    "向量数量:",
    index.ntotal
)

with open("index/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

print("metadata",metadata)

question = "年假需要提前多久申请"
print("question:",question)

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)
query_vector = model.encode(
    question
)

query_vector = np.array(
    [query_vector]
).astype("float32")

distance, ids = index.search(
    query_vector,3 )

# print(f"ids:{ids}")

results = []
for idx in ids[0]:
    item = metadata[idx]
    results.append(item)

context = "\n".join([item["content"] for item in results])

prompt = rag.build_prompt(
    context, question)

# print(f"prompt:{prompt}")

load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)
msg = [
    {
        "role":"user",
        "content":prompt
    }
]

response = client.chat.completions.create(model = MODEL, messages = msg)
print(f"AI回答：{response.choices[0].message.content}")

sources = set(
    result["source"]
    for result in results
)

for source in sources:
    print(
        f"来源:{source}"
    )



from sentence_transformers import SentenceTransformer
from retriever import Retriever
from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os
from generator import Generator

load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)

model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)

index_path = "index/faiss_index"
metadata_path = "index/metadata.json"

retriever = Retriever(model, index_path, metadata_path)

question = "年假需要提前多久申请"

generator = Generator(
    client,
    MODEL
)

results = retriever.search(question, top_k=3)

for result in results:
    print(result)

answer = generator.generate_answer(
    question,
    results
)

print(answer)
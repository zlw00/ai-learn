from dotenv import load_dotenv
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from fastapi.responses import StreamingResponse

from services import retriever
from services import generator
from zhipuai import ZhipuAI
import os
from services import rag_service

from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    question: str

app = FastAPI(
    title="Enterprise RAG API"
)

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")  #Embedding 向量模型

index_path = "index/faiss_index"
metadata_path = "index/metadata.json"
retriever = retriever.Retriever(model, index_path, metadata_path)
load_dotenv()
client = ZhipuAI(
    api_key=os.getenv(
        "ZHIPU_API_KEY"
    )
)
generator = generator.Generator("glm-4-flash", client)

rag_service = rag_service.RagService(retriever, generator, client)

@app.post("/chat")
def chat(request: ChatRequest):
    return rag_service.chat(request.session_id, request.question)

@app.post("/chat/stream")
def chat(request: ChatRequest):
    generator = rag_service.chat_stream(
        request.session_id,
        request.question
    )
    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )
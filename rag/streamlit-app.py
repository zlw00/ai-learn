import streamlit as st
from sentence_transformers import SentenceTransformer

from retriever import Retriever
from generator import Generator
from dotenv import load_dotenv
import os
from zhipuai import ZhipuAI
from pathlib import Path
from index_builder import build_index

load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)
st.title("企业知识库问答助手")

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "BAAI/bge-small-zh-v1.5"
    )

model = load_embedding_model()
index_path = "index/faiss_index"
metadata_path = "index/metadata.json"

uploaded_file = st.file_uploader("上传知识库文件", type=["txt"])
if uploaded_file:
    save_dir = Path("knowledge")
    save_dir.mkdir(
        exist_ok=True
    )
    file_path = save_dir / uploaded_file.name
    file_path.write_bytes(uploaded_file.getvalue())  # 读取网页上传文件的全部二进制内容，保存到本地磁盘 `save_path` 这个文件。
    st.success(
        f"文件保存成功: {file_path}"
    )
    if st.button("构建知识库"):
        build_index(
            file_path
        )

        st.success(
            "知识库构建完成"
        )

question = st.text_input(
    "请输入你的问题"
)

retriever = Retriever(model, index_path, metadata_path)
generator = Generator(
    MODEL,
    client
)

if st.button("查询"):
    results = retriever.search(question, 3)
    answer = generator.generate_answer(question, results)
    st.write(
        answer
    )
    if results:
        st.subheader(
            "参考来源"
        )
        sources = set(item["source"] for item in results)
        for source in sources:
            st.write(source)

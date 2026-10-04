import os
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import json
from zhipuai import ZhipuAI

load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
MESSAGE_FILE = Path("message.json")
client = ZhipuAI(api_key=key)

st.title("流式聊天助手")

def load_messages():
    if not MESSAGE_FILE.exists():
        return []
    try:
        return json.loads(MESSAGE_FILE.read_text(encoding="utf-8"))
    except json.decoder.JSONDecodeError:
        st.warning("message已经损坏，开启全新对话")
        return []

def save_messages(messages):
    MESSAGE_FILE.write_text(json.dumps(messages, ensure_ascii=False), encoding="utf-8")

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("请输入内容:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        stream = client.chat.completions.create(model=MODEL, messages=st.session_state.messages, stream=True)
        with st.chat_message("assistant"):
            respone_container = st.empty()
            fill_ans = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    fill_ans += chunk.choices[0].delta.content
                    respone_container.write(fill_ans)
        st.session_state.messages.append({"role": "assistant", "content": fill_ans})
        save_messages(st.session_state.messages)
    except Exception as e:
        st.session_state.messages.pop()
        print(f"调用模型失败：{e}")

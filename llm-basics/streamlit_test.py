import json
import os

import streamlit as st
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from pathlib import Path

# 页面标题

# st.title("我的AI聊天小应用")
# user_input = st.chat_input("请输入你的问题...")
#
# if user_input:
#     st.chat_message("user").write(user_input)
#     st.chat_message("assistant").write("收到你的消息：" + user_input)


 # 保存对话：
# st.title("我的AI聊天小应用")
#
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])
#
# # 聊天输入框，用户在这里打字提问
# user_input = st.chat_input("请输入你的问题...")
#
# # 判断用户有没有输入内容
# if user_input:
#     #把用户消息加入session_state中
#     st.session_state.messages.append({"role":"user","content":user_input})
#     with st.chat_message("user"):
#         st.write(user_input)
#
#     reply = f"收到你的消息：{user_input}"
#     st.session_state.messages.append({"role":"assistant","content":reply})
#     with st.chat_message("assistant"):
#         st.write(reply)


## 接入ai 替换模拟回复
load_dotenv()
key = os.getenv("ZHIPU_API_KEY")
MODEL = "glm-4-flash"
client = ZhipuAI(api_key=key)
MESSAGE_FILE = Path("message.json")

st.title("聊天对话")

def load_messages():
   if not MESSAGE_FILE.exists():
       return []
   try:
       return json.loads(MESSAGE_FILE.read_text(encoding="utf-8"))
   except json.JSONDecodeError:
       st.warning("message已经损坏，开启全新对话")
       return []

def save_messages(messages):
    MESSAGE_FILE.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("请输入对话内容:")

if user_input:
    input = {"role": "user", "content": user_input}
    st.session_state.messages.append(input)
    with st.chat_message("user"):
        st.write(user_input)
    try:
        response = client.chat.completions.create(model=MODEL, messages=st.session_state.messages)
        ans = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
        save_messages(st.session_state.messages)

    except Exception as e:
        st.session_state.messages.pop()
        print(f"调用模型失败：{e}")
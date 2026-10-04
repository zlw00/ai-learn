from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
from zhipuai import ZhipuAI
import os

load_dotenv()
MODEL = "glm-4-flash"
key = os.getenv("ZHIPU_API_KEY")
MESSAGE_FILE = Path("message.json")
client = ZhipuAI(api_key=key)

st.title("英文邮件润色助手")
st.subheader("输入你的邮件草稿，一键优化语法、措辞与句式")

style_option = st.selectbox("请选择邮件的用途",["正式商务","日常简洁","委婉语气"])

input_email = st.text_area("原始邮件", height=300, placeholder="粘贴你的英文邮件草稿在这里...")

polish_button = st.button("开始润色")
if polish_button:
    if not input_email.strip():
        st.warning("请输入邮件内容")
    elif not key:
        st.error("未读取到ZHIPU_API_KEY，请检查.env文件")
    else:
        system_prompt = f'''你是一个专业的英文邮件润色专家。
        任务：只润色用户提供的邮件原文，不能凭空写邮件。
        ⚠️重要规则：
            1. 如果用户输入文字过少、不是邮件草稿，请直接回复：「输入内容太短，请粘贴完整邮件草稿再润色」
            2. 只修改语法、用词，保留用户原本全部意思，不要额外增加原文不存在的内容
            3. 输出分为两部分：①润色后的邮件 ②简短修改说明
        风格要求：{style_option}'''

        msg = [{"role": "system", "content": system_prompt},
               {"role": "user", "content": input_email}]

        with st.spinner("正在润色，请稍等..."):
            try:
                stream = client.chat.completions.create(model=MODEL, messages=msg, stream=True)
                st.markdown("### 润色完成")
                respone_ans = st.empty()
                full_text = ""
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_text += chunk.choices[0].delta.content
                        respone_ans.write(full_text)
            except Exception as e:
                st.error(f"调用模型失败{e}")



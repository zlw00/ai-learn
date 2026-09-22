import os
from dotenv import load_dotenv
from pathlib import Path
import json
from zhipuai import ZhipuAI


load_dotenv()
MODEL = "glm-4-flash"
MESSAGE_FILE = Path("message.json")
key = os.getenv("ZHIPU_API_KEY")
client = ZhipuAI(api_key=key)

def load_messages():
    if not MESSAGE_FILE.exists():
        return [{
            "role":"system",
            "content":"你是一个友好，简洁的学习助手",
        }]
    try:
        return json.loads(MESSAGE_FILE.read_text())
    except json.JSONDecodeError:
        print("文件格式错误，将开启一段新的对话")
        return [{
            "role":"system",
            "content":"你是一个友好，简洁的学习助手",
        }]


def save_messages(messages):
    MESSAGE_FILE.write_text(json.dumps(messages, ensure_ascii=False, indent=2),encoding="utf-8")


def main():
    print("AI 聊天已启动。输入“退出”结束对话。")
    msg = load_messages()
    while True:
        question = input("\n你:").strip()
        if question == "":
            print("请输入内容")
            continue
        elif question in {"退出","quit","exit"}:
            print("聊天已结束")
            break

        msg.append({
            "role":"user",
            "content":question,
        })
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=msg,
            )

            ans = response.choices[0].message.content
            print(f"AI:{ans}")
            msg.append({
                "role":"assistant",
                "content":ans,
            })
            save_messages(msg)
        except Exception as e:
            msg.pop()
            print(f"调用模型失败：{e}")


if __name__ == "__main__":
    main()

# 连续对话，理解并保存 messages。

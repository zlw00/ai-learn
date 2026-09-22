# AI Chat CLI
一个命令行 AI 聊天程序。

## 项目目标
在终端和大模型一问一答，后续扩展多轮对话。

## 计划功能
- 用户在终端输入问题
- Python读取API密钥，调用大模型API
- 在终端打印模型返回回答
- 后续加入多轮对话记录

## 执行流程
`input() → Python SDK → 模型API → 返回回答 → print()`

## 环境依赖
- python-dotenv：读取.env环境变量
- zhipuai：智谱官方SDK

## 运行方法
1. 在项目根目录新建 `.env` 文件，填入API KEY

## 每个类的功能
- app.py:是一次对话
- continuous_dialogue.py:实现连续对话
from sentence_transformers import CrossEncoder

print("1. 开始加载模型")

model = CrossEncoder(
    "BAAI/bge-reranker-base"
)

print("2. 模型加载完成")

question = "几点打卡"

documents = [
    "工每天需要9点前打卡",
    "员工迟到需要提交说明",
    "年假需要提前3个工作日申请"
]

print("3. 开始计算")

scores = model.predict(
    [
        [question, document]
        for document in documents
    ]
)

print("4. 计算完成")

for document, score in zip(documents, scores):
    print(score, document)
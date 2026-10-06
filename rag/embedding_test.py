from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)


text = "年假需要提前多久申请"


vector = model.encode(text)


print(vector)
print(len(vector))
def split_text(
        text,
        chunk_size,
        overlap
):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


text = """员工申请年假需要提前3个工作日提交审批，审批通过后才能休假。公司员工每年享受带薪年假。"""

chunks = split_text(
    text,
    chunk_size=20,
    overlap=5
)

for i, chunk in enumerate(chunks):
    print(
        f"chunk {i}:"
    )
    print(chunk)

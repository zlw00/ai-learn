import math


def cosine_similarity(vec1, vec2):

    dot_product = 0

    for a, b in zip(vec1, vec2):
        dot_product += a * b


    norm1 = math.sqrt(
        sum(a * a for a in vec1)
    )

    norm2 = math.sqrt(
        sum(b * b for b in vec2)
    )


    return dot_product / (norm1 * norm2)
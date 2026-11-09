from math import sqrt


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Vector cannot be empty !")
    if len(a) != len(b):
        raise ValueError("no. of elements must be identical !")

    dot_product = 0
    sum_squares_a = 0
    sum_squares_b = 0

    for value_a, value_b in zip(a, b):

        product = value_a * value_b

        dot_product += product 
        
        sum_squares_a += value_a**2
        sum_squares_b += value_b**2

    sqrt_a = sqrt(sum_squares_a)
    sqrt_b = sqrt(sum_squares_b)
        
    if sqrt_a == 0 or sqrt_b == 0:
        raise ValueError("Vector length cannot be zero")

    result = dot_product / (sqrt_a * sqrt_b)
    
    return result


def rank_by_similarity(
    query_vector: list[float],
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    if top_k <= 0:
        raise ValueError("top_k is not positive")

    results = []

    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["embedding"])
        results.append({"score": score, "chunk": chunk})
    
    results.sort(key=lambda result: result["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    print(cosine_similarity([1, 2], [2, 4]))   # Approximately 1
    print(cosine_similarity([1, 0], [0, 1]))   # 0
    print(cosine_similarity([1, 0], [-1, 0]))  # -1
    # print(cosine_similarity([0, 0], [1, 0]))

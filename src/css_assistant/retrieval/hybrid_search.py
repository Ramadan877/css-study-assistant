def extract_ids(results: list[dict]) -> list[tuple[str, int]]:
    identifiers = []

    for result in results:
        chunk = result["chunk"]
        chunk_id = (chunk["document_id"], chunk["chunk_number"])
        identifiers.append(chunk_id)

    return identifiers


def combine_ranks(
    keyword_ids: list[tuple[str, int]], 
    vector_ids: list[tuple[str, int]],
) -> dict[tuple[str, int], float]:

    scores = {}

    for rank, chunk_id in enumerate(keyword_ids, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (60 + rank)

    for rank, chunk_id in enumerate(vector_ids, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (60 + rank)

    return scores 

    
def sort_combined_scores(
    scores: dict[tuple[str, int], float],
) -> list[tuple[tuple[str, int], float]]:
    values = scores.items()
    result = sorted(values, key=lambda item: item[1], reverse=True)

    return result


def build_chunk_lookup(
    keyword_results: list[dict],
    vector_results: list[dict],
) -> dict[tuple[str, int], dict]:
    lookup = {}

    for result in keyword_results + vector_results:
        chunk = result["chunk"]

        chunk_id = (chunk["document_id"], chunk["chunk_number"])
        lookup[chunk_id] = chunk
    return lookup


def get_lookup(sorted_scores: list[tuple[tuple[str, int], float]], 
               lookup: dict[tuple[str, int], dict]
               ) -> list[dict]:
    results = []

    for chunk_id, score in sorted_scores:
        chunk = lookup[chunk_id]
        results.append({"score": score, "chunk": chunk})

    return results


if __name__ == "__main__":
    demo_results = [
        {"score": 0.8, "chunk": {"document_id": "css", "chunk_number": 42}},
        {"score": 0.5, "chunk": {"document_id": "css", "chunk_number": 17}},
    ]
    vector_results = [
    {"score": 0.9, "chunk": {"document_id": "css", "chunk_number": 17}},
    {"score": 0.7, "chunk": {"document_id": "css", "chunk_number": 25}},
]
    keyword_ids = extract_ids(demo_results)
    vector_ids = extract_ids(vector_results)

    scores = combine_ranks(keyword_ids, vector_ids)
    sorted_scores = sort_combined_scores(scores)
    # print(sorted_scores)

    lookup = build_chunk_lookup(demo_results, vector_results)
    # print("Number of IDs: ", len(lookup))
    # print("IDs: ", list(lookup.keys()))
    # print("Chunk 42: ", lookup[("css", 42)])

    lookup_2 = get_lookup(sorted_scores, lookup)
    print(lookup_2)


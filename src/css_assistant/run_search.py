import json

from ingestion.storage import load_chunks
from run_embedding import embedding_client, embedding_test

from retrieval.keyword_search import rank_chunks
from retrieval.vector_search import rank_by_similarity
from retrieval.hybrid_search import (
    extract_ids,
    combine_ranks,
    sort_combined_scores,
    build_chunk_lookup,
    get_lookup,
)

from generation.context import build_context
from generation.llm_config import generate_answer


def answer_question(query: str, embedded_chunks: list[dict]) -> str:
    """Generate an answer using hybrid retrieval."""
    if not query.strip():
        raise ValueError("Question cannot be empty")

    # Embed the question.
    endpoint, model, key = embedding_test()

    query_vector, _query_tokens = embedding_client(
        endpoint=endpoint,
        key=key,
        model=model,
        text=query,
    )

    # Run keyword and vector search.
    keyword_results = rank_chunks(query, embedded_chunks, top_k=5)

    vector_results = rank_by_similarity(
        query_vector,
        embedded_chunks,
        top_k=5,
    )

    # Combine the two rankings.
    keyword_ids = extract_ids(keyword_results)
    vector_ids = extract_ids(vector_results)

    combined_scores = combine_ranks(keyword_ids, vector_ids)
    sorted_scores = sort_combined_scores(combined_scores)

    # Recover the full chunks and keep the top five.
    lookup = build_chunk_lookup(keyword_results, vector_results)
    hybrid_results = get_lookup(sorted_scores, lookup)[:5]

    if not hybrid_results:
        return "I don't have enough information to answer this question."

    context = build_context(hybrid_results)
    return generate_answer(query, context)


def print_results(title: str, results: list[dict]) -> None:
    """Print a compact summary of each retrieved chunk."""
    print(f"\n{title}")
    print("-" * 60)

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(
            "Rank:", rank,
            "| Score:", result["score"],
            "| Page:", chunk["page_number"],
            "| Chunk:", chunk["chunk_number"],
        )

        print("Text preview:", chunk["text"][:300])
        print("-" * 60)


if __name__ == "__main__":
    # Load the saved curriculum chunks and their embeddings.
    embedded_chunks = load_chunks("data/processed/embedded_chunks.json")

    # Load the draft evaluation questions.
    with open("data/evaluation/questions.json", "r", encoding="utf-8") as file:
        cases = json.load(file)

    # Load the embedding configuration once for this run.
    endpoint, model, key = embedding_test()

    print("Loaded chunks:", len(embedded_chunks))
    print("Evaluation questions:", len(cases))

    for case_number, case in enumerate(cases, start=1):
        query = case["question"]

        print("\n" + "=" * 60)
        print("Question", case_number, ":", query)
        print("Expected answerable:", case["answerable"])
        print("Expected page:", case["expected_page"])
        print("=" * 60)

        # 1. Keyword search.
        keyword_results = rank_chunks(
            query,
            embedded_chunks,
            top_k=5,
        )

        # 2. Embed this question and run vector search.
        query_vector, query_tokens = embedding_client(
            endpoint=endpoint,
            key=key,
            model=model,
            text=query,
        )

        vector_results = rank_by_similarity(
            query_vector,
            embedded_chunks,
            top_k=5,
        )

        keyword_ids = extract_ids(keyword_results)
        vector_ids = extract_ids(vector_results)

        combined_scores = combine_ranks(keyword_ids, vector_ids)
        sorted_scores = sort_combined_scores(combined_scores)

        lookup = build_chunk_lookup(keyword_results, vector_results)
        hybrid_results = get_lookup(sorted_scores, lookup)[:5]

        print_results("Keyword results", keyword_results)
        print_results("Vector results", vector_results)
        print_results("Hybrid results", hybrid_results)

        print("Question embedding tokens used:", query_tokens)
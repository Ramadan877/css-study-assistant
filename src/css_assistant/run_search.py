from run_embedding import embedding_client, embedding_test

from retrieval.database_search import load_database_chunks, search_database
from retrieval.keyword_search import rank_chunks
from retrieval.hybrid_search import (
    extract_ids,
    combine_ranks,
    sort_combined_scores,
    build_chunk_lookup,
    get_lookup,
)

from generation.context import build_context
from generation.llm_config import generate_answer


def answer_question(query: str, chunks: list[dict]) -> str:
    if not query.strip():
        raise ValueError("Question cannot be empty")

    # 1. Embed the student's question.
    endpoint, model, key = embedding_test()

    query_vector, _query_tokens = embedding_client(
        endpoint=endpoint,
        key=key,
        model=model,
        text=query,
    )

    # 2. Search the database chunks by keywords and vector similarity.
    keyword_results = rank_chunks(query, chunks, top_k=5)

    vector_results = search_database(
        query_vector,
        embedding_deployment=model,
        top_k=5,
    )

    # 3. Combine both rankings.
    keyword_ids = extract_ids(keyword_results)
    vector_ids = extract_ids(vector_results)

    combined_scores = combine_ranks(keyword_ids, vector_ids)
    sorted_scores = sort_combined_scores(combined_scores)

    # 4. Recover the complete chunks for the highest-ranked results.
    lookup = build_chunk_lookup(keyword_results, vector_results)
    hybrid_results = get_lookup(sorted_scores, lookup)[:5]

    if not hybrid_results:
        return "I don't have enough information to answer this question."

    # 5. Generate an answer from the retrieved passages.
    context = build_context(hybrid_results)
    return generate_answer(query, context)


if __name__ == "__main__":
    chunks = load_database_chunks()

    question = (
        "Is there a presentation I need to give "
        "before handing in my dissertation?"
    )

    print("Chunks loaded from PostgreSQL:", len(chunks))
    print("Question:", question)
    print("\nAnswer:", answer_question(question, chunks))
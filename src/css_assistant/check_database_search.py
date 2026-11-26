from run_embedding import embedding_client, embedding_test
from retrieval.database_search import search_database


if __name__ == "__main__":
    question = (
        "Is there a presentation I need to give "
        "before handing in my dissertation?"
    )

    endpoint, model, key = embedding_test()

    question_vector, tokens = embedding_client(
        endpoint=endpoint,
        key=key,
        model=model,
        text=question,
    )

    results = search_database(question_vector, model, top_k=5)

    print("Question:", question)
    print("Question embedding tokens:", tokens)

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(f"\nRank: {rank}")
        print("Similarity:", result["score"])
        print("Page:", chunk["page_number"])
        print("Chunk:", chunk["chunk_number"])
        print("Text:", chunk["text"])
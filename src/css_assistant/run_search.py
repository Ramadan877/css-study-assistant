from ingestion.storage import load_chunks
from run_embedding import embedding_client, embedding_test
from retrieval.vector_search import rank_by_similarity
from generation.context import build_context
from generation.llm_config import generate_answer


def answer_question(query: str, embedded_chunks: list[dict]) -> str:
    
    # --- Embedding ---    
    endpoint, model, key = embedding_test()

    query_vector, query_tokens = embedding_client(
    endpoint=endpoint,
    key=key,
    model=model,
    text=query,
    )
    
    # --- Ranking ---
    vector_results = rank_by_similarity(
        query_vector,
        embedded_chunks,
        top_k=5,
    )

    context = build_context(vector_results)
    print("\nContext:\n", context)
        
    answer = generate_answer(query, context)

    return answer

if __name__ == "__main__":
    embedded_chunks = load_chunks("data/processed/embedded_chunks.json")
    # print("Loaded chunks:", len(chunks))

    query = "What are the prices of the Cafeteria"

    print(answer_question(query, embedded_chunks))


    # # --- Keyword search ---
    # keyword_results = rank_chunks(query, chunks, top_k=5)

    # print("\nKeyword search results:")

    # for rank, result in enumerate(keyword_results, start=1):
    #     chunk = result["chunk"]
    #     shared_words = tokenize(query) & tokenize(chunk["text"])

    #     print("---")
    #     print("Rank:", rank)
    #     print("Score:", result["score"])
    #     print("Page:", chunk["page_number"])
    #     print("Chunk:", chunk["chunk_number"])
    #     print("Shared words:", sorted(shared_words))
    #     print("Text:", chunk["text"])


        # print("\nVector search results: \n")

    
        # for rank, result in enumerate(vector_results, start=1):
        #     chunk = result["chunk"]
        
        #     print("---")
        #     print("Rank:", rank)
        #     print("Score:", result["score"])
        #     print("Page:", chunk["page_number"])
        #     print("Chunk:", chunk["chunk_number"])
        #     print("Text:", chunk["text"])
        
        # print("Question tokens used:", query_tokens) 
from ingestion.storage import load_chunks
from retrieval.keyword_search import rank_chunks, tokenize

from run_embedding import embedding_client, embedding_test
from retrieval.vector_search import rank_by_similarity


if __name__ == "__main__":
    chunks = load_chunks("data/processed/chunks.json")
    print("Loaded chunks:", len(chunks))

    query = "What must I complete before registering for the final master's examination?"
    print("Query:", query)

    # --- Keyword search ---
    keyword_results = rank_chunks(query, chunks, top_k=5)

    print("\nKeyword search results:")

    for rank, result in enumerate(keyword_results, start=1):
        chunk = result["chunk"]
        shared_words = tokenize(query) & tokenize(chunk["text"])

        print("---")
        print("Rank:", rank)
        print("Score:", result["score"])
        print("Page:", chunk["page_number"])
        print("Chunk:", chunk["chunk_number"])
        print("Shared words:", sorted(shared_words))
        print("Text:", chunk["text"])

    # --- Vector search ---
    
    embedded_chunks = load_chunks("data/processed/embedded_chunks.json")
    endpoint, model, key = embedding_test()
    
    questions = [
    "Is there a presentation I need to give before handing in my dissertation?",
    "What must I complete before registering for the final master's examination?",
    "How much does the university cafeteria charge for lunch?",
    ]

    for query in questions:

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
        print("\n")
        print(50 * "#")
        print("Query:", query)
        print(50 * "#")
        print("\n")

        print("\nVector search results:")
    
        for rank, result in enumerate(vector_results, start=1):
            chunk = result["chunk"]
        
            print("---")
            print("Rank:", rank)
            print("Score:", result["score"])
            print("Page:", chunk["page_number"])
            print("Chunk:", chunk["chunk_number"])
            print("Text:", chunk["text"])
        
        print("Question tokens used:", query_tokens) 
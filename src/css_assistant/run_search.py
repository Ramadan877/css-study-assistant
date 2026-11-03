from ingestion.storage import load_chunks
from retrieval.keyword_search import search_chunks, rank_chunks, tokenize


if __name__ == "__main__":
    chunks = load_chunks("data/processed/chunks.json")
    print("Loaded chunks:", len(chunks))
    
    query = "Is there a presentation I need to give before handing in my dissertation?"

    # matches = search_chunks("What are the requirements for the master's thesis?", chunks)
    # print("Matching chunks:", len(matches))
    # for match in matches:
    #     print({"Page_Number": match["page_number"], "Chunk_Number": match["chunk_number"]})
    #     print(match["text"][:300])
    
    ranked_chunks = rank_chunks(query, chunks, 5)
    
    print("Query: ", query)
    for result in ranked_chunks:
        chunk = result["chunk"]
        shared_words = tokenize(query) & tokenize(chunk["text"])
        print( 20 * "---")
        print("Chunk:", chunk["chunk_number"])
        print("Shared words:", sorted(shared_words))
        print("Score:", result["score"], "Page:", chunk["page_number"])
        print(chunk["text"][:300])
        print( 20 * "---")
    
    
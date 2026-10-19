from ingestion.storage import load_chunks
from retrieval.keyword import search_chunks, rank_chunks

if __name__ == "__main__":
    chunks = load_chunks("data/processed/chunks.json")
    print("Loaded chunks:", len(chunks))
    
    matches = search_chunks("What are the requirements for the master's thesis?", chunks)
    print("Matching chunks:", len(matches))
    for match in matches:
        print({"Page_Number": match["page_number"], "Chunk_Number": match["chunk_number"]})
        print(match["text"][:300])
    
    ranked_chunks = rank_chunks("thesis requirements", chunks, 5)
    print(len(ranked_chunks))
    
    for result in ranked_chunks:
        chunk = result["chunk"]
        print(chunk["text"], result["score"], "Page:", chunk["page_number"])
        # print(chunk["text"][:300])
        print("---")
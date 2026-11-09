from ingestion.storage import load_chunks



if __name__ == "__main__":
    first_record = load_chunks("data/processed/demo_embedding.json")[0]
    print(first_record["text"])
    print(first_record["embedding_deployment"]) 
    print("Dimension count matches:", len(first_record["embedding"]) == first_record["dimensions"])
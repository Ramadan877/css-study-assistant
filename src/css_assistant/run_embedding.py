import os
from dotenv import load_dotenv
from pydantic.config import JsonDict
from ingestion.storage import load_chunks, save_chunks
from openai import OpenAI

from retrieval.vector_search import cosine_similarity
from ingestion.storage import load_chunks, save_chunks

def embedding_test():
    load_dotenv(".env", override=True)
    endpoint = os.getenv("AZURE_EMBEDDING_ENDPOINT")
    key = os.getenv("AZURE_EMBEDDING_API_KEY")
    model = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    if not endpoint or not endpoint.strip():
        raise ValueError("missing endpoint",)
    if not key or not key.strip():
        raise ValueError("missing key")
    if not model or not model.strip():
        raise ValueError("missing model")
    print(f"Configuration is ready !", "\nEndpoint: ", endpoint, "\nmodel: ", model )
    return endpoint, model, key 

def embedding_client(endpoint: str, key: str, model: str, text: str) -> tuple[list[float], int]:

    if not text or not text.strip():
        raise ValueError("text is empty")

    client = OpenAI(
        api_key = key,
        base_url = endpoint.rstrip("/") + "/openai/v1/"
    )

    response = client.embeddings.create(
        model=model, 
        input=text 
    )
    vector = response.data[0].embedding
    tokens = response.usage.total_tokens

    return vector, tokens


if __name__ == "__main__":
    endpoint, model, key = embedding_test()
    # vector, tokens = embedding_client(
    #     endpoint=endpoint, 
    #     key=key, 
    #     model=model, 
    #     text="Students present their research concept before submitting their thesis."
    #     )
    # print("Dimensions: ", len(vector))
    # print("First five values: ", vector[:5])
    # print("Tokens used: ", tokens)

    loaded_chunks = load_chunks("data/processed/chunks.json")
    
    embedded_records = []
    total_tokens = 0

    for chunk in loaded_chunks:
        vector, tokens = embedding_client(
            endpoint=endpoint,
            key=key,
            model=model,
            text=chunk["text"]
        )
        embedded_chunk = chunk.copy()
        embedded_chunk["embedding"] = vector 
        embedded_chunk["embedding_deployment"] = model
        embedded_chunk["dimensions"] = len(vector)
        embedded_records.append(embedded_chunk)
        total_tokens += tokens
        save_chunks(embedded_records, "data/processed/embedded_chunks.json") 
        print("Chunk number:", chunk["chunk_number"])
        print(len(embedded_records))
        
    loaded_list = load_chunks("data/processed/embedded_chunks.json")

    print("Loaded records:", len(loaded_list))
    for record in loaded_list:
        print("Document:", record["document_id"])
        print("Chunk:", record["chunk_number"])
        print("Dimensions:", len(record["embedding"]))

    print(loaded_list == embedded_records)
    print("Total tokens:", total_tokens)

    # loaded_chunk = loaded_list[0]

    #     print("Loaded records:", len(loaded_list))
    #     print("Document:", loaded_chunk["document_id"])
    #     print("Page:", loaded_chunk["page_number"])
    #     print("Chunk:", loaded_chunk["chunk_number"])
    #     print("Dimensions:", len(loaded_chunk["embedding"]))
    #     print("Saved data matches:", loaded_list == saved_list)
    #     print("Tokens used:", tokens)



    # question_vector, question_tokens = embedding_client(
    #     endpoint=endpoint,
    #     key=key,
    #     model=model,
    #     text="Is there a presentation I need to give before handing in my dissertation?"
    # )

    # passage_text = (
    #     "Students must present the research concept of their master's thesis "
    #     "in the master's thesis colloquium seminar before submitting the completed thesis."
    # )
    # passage_vector, passage_tokens = embedding_client(
    #     endpoint=endpoint,
    #     key=key,
    #     model=model,
    #     text=passage_text
    #     )

    # passage_dict = {"text": passage_text, "embedding": passage_vector, "embedding_deployment": model, "dimensions": len(passage_vector)}
    # print(passage_dict["text"])
    # print(passage_dict["embedding_deployment"])
    # print("Dimensions: ", passage_dict["dimensions"])

    # records_to_save = [passage_dict]

    # save_chunks(records_to_save, "data/processed/demo_embedding.json")

    # loaded_records = load_chunks("data/processed/demo_embedding.json")
    # print("Loaded records:", len(loaded_records))
    # print("Dimensions:", len(loaded_records[0]["embedding"]))
    # print("Saved data matches:", loaded_records == records_to_save)


    # score = cosine_similarity(question_vector, passage_vector)
    # print("Similarity:", score)

    # unrelated_vector, unrelated_tokens = embedding_client(
    #     endpoint=endpoint,
    #     key=key,
    #     model=model,
    #     text="The cafeteria serves lunch from noon until two."
    # )

    # score = cosine_similarity(question_vector, unrelated_vector)
    # print("Similarity:", score)
    # print("Total tokens:", question_tokens + passage_tokens + unrelated_tokens)
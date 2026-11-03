import os
from dotenv import load_dotenv
from openai import OpenAI

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
    vector, tokens = embedding_client(
        endpoint=endpoint, 
        key=key, 
        model=model, 
        text="Students present their research concept before submitting their thesis."
        )
    print("Dimensions: ", len(vector))
    print("First five values: ", vector[:5])
    print("Tokens used: ", tokens)

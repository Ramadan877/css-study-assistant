import json
import os

import psycopg
from dotenv import load_dotenv


def import_chunks():
    load_dotenv(".env")

    password = os.getenv("CSS_DB_PASSWORD")
    if not password or not password.strip():
        raise ValueError("CSS_DB_PASSWORD is missing from .env")

    # These records already include the text, metadata, and embeddings.
    with open("data/processed/embedded_chunks.json", "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print("Records loaded from JSON:", len(chunks))

    with psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="css_assistant",
        user="css_user",
        password=password,
    ) as connection:
        with connection.cursor() as cursor:
            inserted = 0

            for chunk in chunks:
                embedding = chunk["embedding"]

                if len(embedding) != 1536:
                    raise ValueError(
                        f"Chunk {chunk['chunk_number']} has "
                        f"{len(embedding)} dimensions; expected 1536."
                    )

                cursor.execute(
                    """
                    INSERT INTO chunks (
                        document_id,
                        chunk_number,
                        page_number,
                        source_url,
                        text,
                        embedding_deployment,
                        embedding
                        )
                    VALUES (%s, %s, %s, %s, %s, %s, %s::vector)
                    ON CONFLICT (document_id, chunk_number) DO NOTHING
                    """,
                    (
                        chunk["document_id"],
                        chunk["chunk_number"],
                        chunk["page_number"],
                        chunk["source_url"],
                        chunk["text"],
                        chunk["embedding_deployment"],
                        json.dumps(embedding),
                    ),
                )

                inserted += cursor.rowcount

            cursor.execute("SELECT COUNT(*) FROM chunks;")
            total = cursor.fetchone()[0]

        print("New records inserted:", inserted)
        print("Total records in database:", total)


if __name__ == "__main__":
    import_chunks()
    
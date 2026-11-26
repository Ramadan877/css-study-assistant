import json
import os

import psycopg
from dotenv import load_dotenv


def search_database(
    query_vector: list[float],
    embedding_deployment: str,
    top_k: int = 5,
) -> list[dict]:
    if len(query_vector) != 1536:
        raise ValueError("The question embedding must have 1536 dimensions")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    load_dotenv(".env")
    password = os.getenv("CSS_DB_PASSWORD")

    if not password or not password.strip():
        raise ValueError("CSS_DB_PASSWORD is missing from .env")

    # Convert the Python list to a format PostgreSQL can cast to a vector.
    vector_string = json.dumps(query_vector)

    with psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="css_assistant",
        user="css_user",
        password=password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    document_id,
                    chunk_number,
                    page_number,
                    source_url,
                    text,
                    1 - (embedding <=> %s::vector) AS score
                FROM chunks
                WHERE embedding_deployment = %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (vector_string, embedding_deployment, vector_string, top_k),
            )

            rows = cursor.fetchall()

    results = []

    for document_id, chunk_number, page_number, source_url, text, score in rows:
        results.append(
            {
                "score": score,
                "chunk": {
                    "document_id": document_id,
                    "chunk_number": chunk_number,
                    "page_number": page_number,
                    "source_url": source_url,
                    "text": text,
                },
            }
        )

    return results


def load_database_chunks() -> list[dict]:
    """Load chunk text and metadata for keyword search."""
    load_dotenv(".env")
    password = os.getenv("CSS_DB_PASSWORD")

    if not password or not password.strip():
        raise ValueError("CSS_DB_PASSWORD is missing from .env")

    with psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="css_assistant",
        user="css_user",
        password=password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT document_id, chunk_number, page_number, source_url, text
                FROM chunks
                ORDER BY document_id, chunk_number
                """
            )
            rows = cursor.fetchall()

    return [
        {
            "document_id": document_id,
            "chunk_number": chunk_number,
            "page_number": page_number,
            "source_url": source_url,
            "text": text,
        }
        for document_id, chunk_number, page_number, source_url, text in rows
    ] 
import os

from dotenv import load_dotenv
import psycopg


if __name__ == "__main__":
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
            cursor.execute("SELECT COUNT(*) FROM chunks;")
            count = cursor.fetchone()[0]

    print("Connected to PostgreSQL successfully!")
    print("Chunks in database:", count)
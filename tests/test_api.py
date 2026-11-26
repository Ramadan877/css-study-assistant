from fastapi.testclient import TestClient

import main
from main import app


client = TestClient(app)


def test_blank_question_returns_422():
    response = client.post("/questions", json={"question": "  "})

    assert response.status_code == 422


def test_valid_question(monkeypatch):
    fake_chunks = [{"chunk_number": 1}]

    def fake_load_database_chunks():
        return fake_chunks

    def fake_answer_question(query, chunks):
        assert query == "What is CSS?"
        assert chunks == fake_chunks
        return "Test answer"

    monkeypatch.setattr(main, "load_database_chunks", fake_load_database_chunks)
    monkeypatch.setattr(main, "answer_question", fake_answer_question)

    response = client.post(
        "/questions",
        json={"question": "What is CSS?"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}
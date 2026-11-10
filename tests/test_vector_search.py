import pytest 
from src.css_assistant.retrieval.vector_search import cosine_similarity, rank_by_similarity

def test_same_direction():
    result = cosine_similarity([1, 0], [2, 0])
    assert result == pytest.approx(1.0)

def test_perpendicular():
    result = cosine_similarity([1, 0], [0, 1])
    assert result == pytest.approx(0.0)

def test_zero_vector():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 0])

def test_rank_by_similarity():

    chunks = [
        {"chunk_number": 1, "embedding": [0, 1]},
        {"chunk_number": 2, "embedding": [1, 0]}
    ]

    query_vector = [1, 0]
    results = rank_by_similarity(query_vector, chunks, top_k=1)

    assert len(results) == 1
    assert results[0]["chunk"]["chunk_number"] == 2
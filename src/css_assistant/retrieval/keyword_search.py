import re


STOP_WORDS = {"a", "an", "the", "is", "are", "what", "for", "of", "to", "and", "s"}

def search_chunks(query: str, chunks: list[dict]) -> list[dict]:
    query = query.strip().lower()

    if not query:
        raise ValueError("query is empty !!")

    matches_list = []

    for chunk in chunks:
        chunk_text = chunk["text"].lower()
        if query in chunk_text:
            matches_list.append(chunk)

    return matches_list

def score_overlap(query: str, text: str) -> int:
    query_words = tokenize(query)
    text_words = tokenize(text)
    shared_words = query_words & text_words 
    return len(shared_words)

def rank_chunks(query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    if not query.strip():
        raise ValueError("query must not be blank")

    results = []
    for chunk in chunks:
        chunk_score = score_overlap(query, chunk["text"])
        if chunk_score > 0:
            results.append({"score": chunk_score, "chunk": chunk})

    results.sort(key=lambda result: result["score"], reverse=True)
    return results[:top_k]


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z]+", text.lower()) 
    set_words = set(words)
    set_words = set_words - STOP_WORDS
    return set_words

if __name__ == "__main__":
    chunks = [
        {"document_id": "demo", "page_number": 1, "chunk_number": 1,
        "source_url": "https://example.com/demo.pdf",
        "text": "The master's thesis requires independent research."},
        {"document_id": "demo", "page_number": 2, "chunk_number": 2,
        "source_url": "https://example.com/demo.pdf",
        "text": "Students select elective courses."},
    ]
    # print(search_chunks(" elective ", chunks))
    print(score_overlap("thesis research", "THESIS thesis research methods"))
    print(rank_chunks("thesis research", chunks, top_k=5))
    print(tokenize("thesis, requirements?"))
    print(tokenize("THESIS thesis"))
    print(tokenize("!!!"))
    print(tokenize("the and for"))
    print(tokenize("not before submission"))

    print(score_overlap("THESIS, requirements?", "Thesis requirements."))
    print(score_overlap("thesis thesis", "thesis"))
    print(score_overlap("scholarship", "thesis requirements"))
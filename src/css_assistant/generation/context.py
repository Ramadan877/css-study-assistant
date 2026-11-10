

def build_context(results: list[dict]) -> str:
    passages = []

    for result in results:
        chunk = result["chunk"]
        passage_str = (
        f"Page: {chunk["page_number"]}\n"
        f"Source Url {chunk["source_url"]}\n"
        f"Text: {chunk["text"]}"
        )

        passages.append(passage_str)
    
    passages = "\n\n".join(passages)
    return passages


if __name__ == "__main__":
    print(build_context([
        {
        "score": 0.44,
        "chunk": {
            "page_number": 13,
            "source_url": "https://example.com/curriculum.pdf",
            "text": "Students must present their research concept..."
            }
        },
                {
        "score": 0.44,
        "chunk": {
            "page_number": 13,
            "source_url": "https://example.com/curriculum.pdf",
            "text": "xxxxxxxxxxxxxxxxxxxxxxx..."
            }
        }
    ]))
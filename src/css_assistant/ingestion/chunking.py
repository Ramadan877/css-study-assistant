def split_text(text: str, chunk_size: int) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    chunks = []
    for start in range (0, len(text), chunk_size):
        piece = text[start : start + chunk_size]
        chunks.append(piece)
        
    return chunks


def chunk_pages(records: list[dict], chunk_size: int) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    output = []
    chunk_number = 1
    for page in records:
        pieces = split_text(page["text"], chunk_size)

        for piece in pieces:
            metadata = {"document_id": page["document_id"], "source_url": page["source_url"], "page_number": page["page_number"], "chunk_number": chunk_number, "text" : piece}
            output.append(metadata)
            chunk_number += 1
    return output


def verify_chunks(pages: list[dict], chunks: list[dict]) -> bool:
    for original_page in pages:
        match_txt = []
        print("Checking page:", original_page["page_number"])
        print("Original text:", repr(original_page["text"]))
        for chunk in chunks:
            match_id = chunk["document_id"] == original_page["document_id"]
            match_pg_num = chunk["page_number"] == original_page["page_number"]

            print(
                "Checking page:", original_page["page_number"],
                "| Chunk belongs to page:", chunk["page_number"],
                "| Chunk number:", chunk["chunk_number"],
            )

            if match_id and match_pg_num:
                match_txt.append(chunk["text"])
                print("Collected pieces: ", match_txt)
            
        reconstructed_text = "".join(match_txt)

        if reconstructed_text != original_page["text"]:
            return False
    return True




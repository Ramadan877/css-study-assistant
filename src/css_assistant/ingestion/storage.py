import json

def save_chunks(chunks: list[dict], output_path: str) -> None:
    with open(output_path, "w", encoding="UTF-8") as ouf:
        json.dump(chunks, ouf, ensure_ascii=False, indent=2)


def load_chunks(input_path: str) -> list[dict]:
    with open(input_path, "r", encoding="UTF-8") as inf:
        read_list = json.load(inf)
    
    return read_list

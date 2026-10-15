from multiprocessing import Value
from extract_pdf import extract_pages
from chunking import chunk_pages, verify_chunks
from storage import load_chunks, save_chunks
import os

if __name__ == "__main__":
    pages = extract_pages(
        pdf_path="docs/css_curricullum.pdf",
        document_id="css_curriculum_2025_en",
        source_url="https://static.uni-graz.at/fileadmin/_files/_faculty_sites/_sowi/Studienservice/Masterpruefung/CSS/MA_Computational_Social_Systems_Beschluss_Senat_KFU_25062025_TU_23062025_eng-GB_BW.pdf"        
        )
    chunks = chunk_pages(pages, chunk_size=1000)
    is_valid = verify_chunks(pages, chunks)
    print("All page text preserved:", is_valid)

    if not is_valid:
        raise ValueError("Chunk verification failed; output was not saved")

    os.makedirs("data/processed", exist_ok=True)
    save_chunks(chunks, "data/processed/chunks.json")

    loaded_chunks = load_chunks("data/processed/chunks.json")
    print("Loaded chunks:", len(loaded_chunks))
    print("Saved data matches:", loaded_chunks == chunks)

    print("Pages:", len(pages)) 
    print("Chunks:", len(chunks))

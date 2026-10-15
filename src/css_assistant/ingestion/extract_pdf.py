from pypdf import PdfReader 

# def extract_pages(pdf_path: str) -> list[dict]:
#     reader = PdfReader(pdf_path)
#     records = []
#     pages = reader.pages
#     for i, page in enumerate(pages, start=1):
#         text = page.extract_text()
#         if text is None:
#             return ""
#         records.append({"page_number": i, "text": text})

    
#     return records

def extract_pages(
    pdf_path: str,
    document_id: str,
    source_url: str,
    ) -> list[dict]:

    reader = PdfReader(pdf_path)
    records = []
    pages = reader.pages
    for i, page in enumerate(pages, start=1):
        text = page.extract_text()
        if text is None:
            text = ""
        records.append({"page_number": i, "text":text, "document_id": document_id, "source_url": source_url})

    return records

if __name__ == "__main__":
    records = extract_pages(
        pdf_path="docs/css_curricullum.pdf",
        document_id="css_curriculum_2025_en",
        source_url="https://static.uni-graz.at/fileadmin/_files/_faculty_sites/_sowi/Studienservice/Masterpruefung/CSS/MA_Computational_Social_Systems_Beschluss_Senat_KFU_25062025_TU_23062025_eng-GB_BW.pdf"        
        )


    print("number of returned records:", len(records))
    print("first record's page number:", records[0]["page_number"], records[0]["text"][:200])
    print("last record's page number:", records[-1]["page_number"], records[-1]["text"][:200]) 
    print(records[0]["document_id"], records[0]["source_url"])
from pypdf import PdfReader
import re

def pdf_reader(file):
    pdf_reader = PdfReader(file)

    page_content = {}

    for indx, pdf_page in enumerate(pdf_reader.pages):
        page_content[indx + 1] = pdf_page.extract_text()
    
    full_text = " ".join(str(val) for val in page_content.values())
    raw_lines = full_text.split('\n')
    clean_queries = []
    
    for line in raw_lines:
        clean = re.sub(r'[*#\-0-9.]', '', line).strip()
        if clean:
            clean_queries.append(clean)
    

    result =  "\n".join(i for i in clean_queries)
    
    return result
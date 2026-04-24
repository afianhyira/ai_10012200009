import fitz  # PyMuPDF
import os

def load_pdf_data(filepath: str) -> list:
    """
    Load PDF using PyMuPDF and extract text per page.
    Returns a list of dictionaries with page_number and text.
    """
    if not os.path.exists(filepath):
        print(f"Warning: PDF file not found at {filepath}")
        return []
    
    pages_data = []
    try:
        doc = fitz.open(filepath)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text.strip():
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text
                })
        doc.close()
    except Exception as e:
        print(f"Error loading PDF {filepath}: {e}")
        
    return pages_data

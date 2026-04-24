import re
import pandas as pd
from typing import List, Dict, Any
from src.utils.helpers import clean_text, extract_keywords

def chunk_csv_row(row: dict, row_idx: int) -> dict:
    """
    Convert a single CSV row into a readable natural-language chunk.
    """
    # Assuming columns like region, constituency, party, candidate, votes
    # We will build a generic representation but try to make it sound natural
    parts = []
    keywords = []
    
    for key, value in row.items():
        if pd.isna(value) or str(value).strip() == "":
            continue
        cleaned_val = str(value).strip()
        parts.append(f"The {key.replace('_', ' ')} is {cleaned_val}.")
        keywords.extend(extract_keywords(str(cleaned_val)))
        
    text = " ".join(parts)
    
    # Try to find a year for metadata
    year = None
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        year = year_match.group(0)
        
    return {
        "chunk_id": f"csv_row_{row_idx}",
        "source": "Ghana_Election_Result.csv",
        "chunk_type": "csv_row",
        "text": text,
        "keywords": list(set(keywords)),
        "year": year
    }

def process_csv_dataframe(df) -> List[dict]:
    """Process pandas dataframe into chunks."""
    import pandas as pd # Ensure pandas is available locally
    chunks = []
    for idx, row in df.iterrows():
        chunks.append(chunk_csv_row(row.to_dict(), idx))
    return chunks

def fixed_size_chunking(text: str, source: str, page_num: int, chunk_size=400, overlap=80) -> List[dict]:
    """Strategy A: Fixed-size chunking by words."""
    words = text.split()
    chunks = []
    i = 0
    chunk_idx = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        
        chunks.append({
            "chunk_id": f"pdf_fixed_{page_num}_{chunk_idx}",
            "source": source,
            "chunk_type": "pdf_fixed",
            "text": chunk_text,
            "keywords": extract_keywords(chunk_text),
            "year": None # Could extract year similar to CSV
        })
        i += (chunk_size - overlap)
        chunk_idx += 1
    return chunks

def paragraph_aware_chunking(text: str, source: str, page_num: int) -> List[dict]:
    """
    Strategy B: Paragraph-aware chunking.
    Splits by paragraph, merges small paragraphs, targets ~300-500 words.
    """
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk_words = []
    chunk_idx = 0
    
    for p in paragraphs:
        p_clean = clean_text(p)
        if not p_clean:
            continue
            
        p_words = p_clean.split()
        
        if len(current_chunk_words) + len(p_words) <= 500:
            current_chunk_words.extend(p_words)
        else:
            if current_chunk_words:
                chunk_text = " ".join(current_chunk_words)
                chunks.append({
                    "chunk_id": f"pdf_para_{page_num}_{chunk_idx}",
                    "source": source,
                    "chunk_type": "pdf_para",
                    "text": chunk_text,
                    "keywords": extract_keywords(chunk_text),
                    "year": None
                })
                chunk_idx += 1
                # Light sentence overlap: keep last 20 words for context
                current_chunk_words = current_chunk_words[-20:] + p_words
            else:
                # A single paragraph is huge
                current_chunk_words = p_words
                
    if current_chunk_words:
        chunk_text = " ".join(current_chunk_words)
        if len(current_chunk_words) > 30: # Don't keep tiny trailing chunks
            chunks.append({
                "chunk_id": f"pdf_para_{page_num}_{chunk_idx}",
                "source": source,
                "chunk_type": "pdf_para",
                "text": chunk_text,
                "keywords": extract_keywords(chunk_text),
                "year": None
            })
            
    return chunks

def process_pdf_pages(pages_data: List[dict], source: str, strategy="paragraph") -> List[dict]:
    """Process list of page dicts into chunks using specified strategy."""
    chunks = []
    for page in pages_data:
        text = clean_text(page["text"])
        if strategy == "fixed":
            chunks.extend(fixed_size_chunking(text, source, page["page_number"]))
        else:
            chunks.extend(paragraph_aware_chunking(text, source, page["page_number"]))
    return chunks

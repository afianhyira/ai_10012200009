import pytest
from src.preprocessing.chunking import fixed_size_chunking, paragraph_aware_chunking, chunk_csv_row

def test_fixed_size_chunking():
    text = "word " * 450
    chunks = fixed_size_chunking(text, "test.pdf", 1, chunk_size=400, overlap=80)
    assert len(chunks) == 2
    assert len(chunks[0]["text"].split()) == 400
    
def test_paragraph_chunking():
    text = "Paragraph 1.\n\nParagraph 2."
    chunks = paragraph_aware_chunking(text, "test.pdf", 1)
    assert len(chunks) > 0
    
def test_csv_chunking():
    row = {"region": "Ashanti", "votes": 5000}
    chunk = chunk_csv_row(row, 1)
    assert "Ashanti" in chunk["text"]
    assert "5000" in chunk["text"]
    assert chunk["chunk_type"] == "csv_row"

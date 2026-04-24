from src.utils.helpers import clean_text

def clean_pdf_text(raw_text: str) -> str:
    """Apply specific cleaning rules for PDF text (e.g. removing repetitive footers)."""
    text = clean_text(raw_text)
    # Could add rules to remove "Page X of Y" etc.
    return text

import re
from typing import List, Dict

def normalize_scores(scores: List[float]) -> List[float]:
    """Min-Max normalization of a list of scores."""
    if not scores:
        return []
    min_val = min(scores)
    max_val = max(scores)
    if max_val == min_val:
        return [1.0 for _ in scores] if max_val > 0 else [0.0 for _ in scores]
    return [(s - min_val) / (max_val - min_val) for s in scores]

def compute_domain_score(
    chunk: dict,
    query: str,
    query_type: str,
    norm_vector_score: float,
    norm_bm25_score: float,
    weights: dict = None
) -> float:
    """
    Innovation Feature: Domain-specific scoring function.
    Calculates a final score based on multiple signals.
    """
    if weights is None:
        weights = {
            "vector": 0.4,
            "bm25": 0.3,
            "source_match": 0.1,
            "keyword_overlap": 0.1,
            "numeric_bonus": 0.1
        }
        
    query_lower = query.lower()
    
    # 1. Source Match Bonus
    source_match_bonus = 0.0
    if query_type == "Election" and "election" in str(chunk.get("source", "")).lower():
        source_match_bonus = 1.0
    elif query_type == "Budget" and "budget" in str(chunk.get("source", "")).lower():
        source_match_bonus = 1.0
        
    # 2. Keyword Overlap Bonus
    query_words = set(re.findall(r'\b\w+\b', query_lower))
    chunk_keywords = set(chunk.get("keywords", []))
    overlap = query_words.intersection(chunk_keywords)
    # Give up to 1.0 bonus based on overlapping important keywords
    keyword_overlap_bonus = min(len(overlap) / max(1, len(query_words)), 1.0)
    
    # 3. Numeric / Year Bonus
    numeric_bonus = 0.0
    # If query asks for a year and chunk has that year
    year_match = re.search(r'\b(19|20)\d{2}\b', query_lower)
    if year_match and chunk.get("year") == year_match.group(0):
        numeric_bonus = 1.0
    # Or if query has numbers and chunk has those numbers
    numbers_in_query = set(re.findall(r'\b\d+\b', query_lower))
    if numbers_in_query:
        numbers_in_chunk = set(re.findall(r'\b\d+\b', str(chunk.get("text", ""))))
        if numbers_in_query.intersection(numbers_in_chunk):
            numeric_bonus = max(numeric_bonus, 0.8)

    # Final Weighted Sum
    final_score = (
        weights["vector"] * norm_vector_score +
        weights["bm25"] * norm_bm25_score +
        weights["source_match"] * source_match_bonus +
        weights["keyword_overlap"] * keyword_overlap_bonus +
        weights["numeric_bonus"] * numeric_bonus
    )
    
    return final_score

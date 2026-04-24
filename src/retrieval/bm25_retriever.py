from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re

class BM25Retriever:
    def __init__(self, chunks: List[dict]):
        self.chunks = chunks
        
        # Tokenize chunk texts for BM25
        tokenized_corpus = [self._tokenize(chunk["text"]) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer: lowercase and split by non-word characters."""
        return re.findall(r'\b\w+\b', str(text).lower())
        
    def search(self, query: str, top_k=5) -> List[Tuple[dict, float]]:
        """
        Search for top_k most similar chunks using BM25.
        """
        if not self.chunks:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        top_n = min(top_k, len(self.chunks))
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
        
        results = []
        # Normalize BM25 scores roughly (BM25 can go high, we'll just keep raw for now and normalize in scoring.py)
        for idx in top_indices:
            if scores[idx] > 0: # only return matches
                results.append((self.chunks[idx], float(scores[idx])))
                
        return results

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
    def embed_chunks(self, chunks: List[dict]) -> np.ndarray:
        """
        Takes a list of chunk dictionaries and generates embeddings for their text.
        """
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single query."""
        return self.model.encode([query])[0]

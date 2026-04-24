import faiss
import numpy as np
from typing import List, Tuple

class VectorStore:
    def __init__(self, embedding_dim=384):
        """
        Initialize FAISS index. all-MiniLM-L6-v2 produces 384-dimensional embeddings.
        """
        self.embedding_dim = embedding_dim
        # Using IndexFlatIP for Cosine Similarity (assuming embeddings are normalized)
        # or IndexFlatL2 for L2 distance. We'll use L2 for simplicity and invert it for score.
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []
        
    def add_embeddings(self, embeddings: np.ndarray, chunks: List[dict]):
        """Add embeddings and metadata to the store."""
        if len(embeddings) != len(chunks):
            raise ValueError("Number of embeddings must match number of chunks")
            
        self.index.add(embeddings.astype(np.float32))
        self.chunks.extend(chunks)
        
    def search(self, query_embedding: np.ndarray, top_k=5) -> List[Tuple[dict, float]]:
        """
        Search for top_k most similar chunks.
        Returns a list of (chunk, score) tuples.
        """
        if self.index.ntotal == 0:
            return []
            
        query_embedding = query_embedding.astype(np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.chunks):
                # Convert L2 distance to a similarity score (lower dist = higher similarity)
                # Max L2 distance could be around 4 for normalized vectors, so we can do 1 / (1 + dist)
                sim_score = 1.0 / (1.0 + dist)
                results.append((self.chunks[idx], sim_score))
                
        return results

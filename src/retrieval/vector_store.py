import faiss
import numpy as np
import json
import os
from typing import List, Tuple

class VectorStore:
    def __init__(self, embedding_dim=1024):
        """
        Initialize FAISS index. 
        Note: Cohere embed-english-v3.0 produces 1024-dimensional embeddings.
        """
        self.embedding_dim = embedding_dim
        # Using IndexFlatL2 for simplicity
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
        """
        if self.index.ntotal == 0:
            return []
            
        query_embedding = query_embedding.astype(np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.chunks):
                sim_score = 1.0 / (1.0 + dist)
                results.append((self.chunks[idx], sim_score))
                
        return results

    def save_to_disk(self, directory: str, filename_prefix: str = "vector_store"):
        """Save FAISS index and chunks to disk."""
        os.makedirs(directory, exist_ok=True)
        
        # Save FAISS index
        index_path = os.path.join(directory, f"{filename_prefix}.index")
        faiss.write_index(self.index, index_path)
        
        # Save chunks metadata
        chunks_path = os.path.join(directory, f"{filename_prefix}_chunks.json")
        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=4)
            
        print(f"Index and chunks saved to {directory}")

    def load_from_disk(self, directory: str, filename_prefix: str = "vector_store"):
        """Load FAISS index and chunks from disk."""
        index_path = os.path.join(directory, f"{filename_prefix}.index")
        chunks_path = os.path.join(directory, f"{filename_prefix}_chunks.json")
        
        if not os.path.exists(index_path) or not os.path.exists(chunks_path):
            raise FileNotFoundError(f"Index files not found in {directory}")
            
        self.index = faiss.read_index(index_path)
        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
            
        self.embedding_dim = self.index.d
        print(f"Loaded {len(self.chunks)} chunks from disk.")

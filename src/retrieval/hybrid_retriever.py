from typing import List, Dict, Tuple
from src.retrieval.scoring import normalize_scores, compute_domain_score
from src.utils.helpers import get_query_type

class HybridRetriever:
    def __init__(self, vector_store, bm25_retriever, embedder):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.embedder = embedder
        
    def re_rank_rrf(self, vector_results: List[Tuple[dict, float]], bm25_results: List[Tuple[dict, float]], k: int = 60) -> List[Tuple[dict, float]]:
        """
        Reciprocal Rank Fusion (RRF) implementation for re-ranking.
        This provides a robust way to combine different retrieval signals.
        """
        rrf_scores = {}
        chunk_map = {}
        
        # Process Vector Results
        for rank, (chunk, _) in enumerate(vector_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
            
        # Process BM25 Results
        for rank, (chunk, _) in enumerate(bm25_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
            
        # Convert to sorted list of (chunk, score)
        sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [(chunk_map[cid], score) for cid, score in sorted_rrf]

    def retrieve(self, query: str, top_k: int = 4) -> Tuple[List[dict], Dict[str, dict]]:
        """
        Retrieves candidates using both vector search and BM25,
        applies RRF re-ranking, and calculates final scores.
        """
        # Embed query
        query_embedding = self.embedder.embed_query(query)
        
        # Get candidates (retrieve more than top_k for effective re-ranking)
        vector_results = self.vector_store.search(query_embedding, top_k=top_k*5)
        bm25_results = self.bm25_retriever.search(query, top_k=top_k*5)
        
        # Apply RRF Re-ranking (Requirement Part B)
        reranked_results = self.re_rank_rrf(vector_results, bm25_results)
        
        # Calculate domain-specific scores for the top candidates
        query_type = get_query_type(query)
        final_scores = {}
        top_chunks = []
        
        for chunk, rrf_score in reranked_results[:top_k]:
            cid = chunk["chunk_id"]
            
            # Find raw scores for telemetry (default to 0 if not present)
            v_score = next((s for c, s in vector_results if c["chunk_id"] == cid), 0.0)
            b_score = next((s for c, s in bm25_results if c["chunk_id"] == cid), 0.0)
            
            # Normalize for final report
            # (In a real RRF implementation, the RRF score itself is the final score, 
            # but we'll scale it for UI visibility)
            norm_v = v_score if v_score > 0 else 0.0
            norm_b = b_score if b_score > 0 else 0.0
            
            # We combine RRF with domain-specific boosts for the perfect retrieval
            final_score = rrf_score + compute_domain_score(chunk, query, query_type, norm_v, norm_b)
            
            final_scores[cid] = {
                "vector_score": norm_v,
                "bm25_score": norm_b,
                "rrf_score": rrf_score,
                "final_score": final_score
            }
            top_chunks.append(chunk)
            
        return top_chunks, final_scores

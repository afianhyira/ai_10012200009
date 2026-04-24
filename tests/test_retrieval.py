import pytest
import numpy as np
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.scoring import compute_domain_score

def test_vector_store():
    store = VectorStore(embedding_dim=2)
    # mock embeddings
    embeddings = np.array([[1.0, 0.0], [0.0, 1.0]])
    chunks = [{"chunk_id": "1", "text": "A"}, {"chunk_id": "2", "text": "B"}]
    store.add_embeddings(embeddings, chunks)
    
    # Search with [1.0, 0.0] should return chunk 1 first
    results = store.search(np.array([1.0, 0.0]), top_k=1)
    assert len(results) == 1
    assert results[0][0]["chunk_id"] == "1"

def test_bm25_retriever():
    chunks = [{"chunk_id": "1", "text": "election results are here"}, {"chunk_id": "2", "text": "budget is large"}]
    retriever = BM25Retriever(chunks)
    results = retriever.search("election", top_k=1)
    assert len(results) == 1
    assert results[0][0]["chunk_id"] == "1"

def test_domain_scoring():
    chunk = {"source": "Ghana_Election_Result.csv", "keywords": ["election", "vote"]}
    score = compute_domain_score(
        chunk=chunk,
        query="who won the election?",
        query_type="Election",
        norm_vector_score=0.8,
        norm_bm25_score=0.5
    )
    # 0.4*0.8 + 0.3*0.5 + 0.1(source) + 0.1(keyword overlap)
    # Should be > 0
    assert score > 0

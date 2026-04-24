# Architecture Design

## Overview
This custom RAG system is designed specifically for answering questions about the 2025 Ghana Budget and Election Results. It strictly avoids any high-level RAG frameworks (like LangChain or LlamaIndex) and implements the pipeline manually.

## Component Interaction
1. **Document Ingestion (`load_csv.py`, `load_pdf.py`)**
   - Extracts raw data into standard list/dict formats.
2. **Preprocessing & Chunking (`chunking.py`)**
   - Applies domain-specific chunking. The PDF uses paragraph-aware splitting to retain semantic boundaries, while the CSV is translated row-by-row into natural language.
3. **Embeddings & Vector Store (`embedder.py`, `vector_store.py`)**
   - Uses `all-MiniLM-L6-v2` to convert chunks into 384-dimensional dense vectors.
   - Vectors are indexed manually using FAISS (`IndexFlatL2`) for fast top-k similarity search.
4. **Keyword Search (`bm25_retriever.py`)**
   - A secondary index using the Okapi BM25 algorithm to capture exact keyword matches which dense vectors sometimes miss.
5. **Hybrid Scoring (`hybrid_retriever.py`, `scoring.py`)**
   - Merges results from FAISS and BM25.
   - Normalizes scores.
   - Applies the **Innovation Feature**: Domain-Specific Scoring (adding bonuses for source matching, keyword overlap, and numeric values).
6. **Prompt Generation (`prompt_builder.py`)**
   - Formats the retrieved context.
   - Wraps it in strict grounding rules to prevent hallucination.
7. **LLM Client (`llm_client.py`)**
   - Sends the engineered prompt to OpenAI for final answer generation.

## Data Flow Diagram (Placeholder)
*(Insert Mermaid diagram or image here showing User Query -> Hybrid Retriever -> Prompt Builder -> LLM -> Response)*

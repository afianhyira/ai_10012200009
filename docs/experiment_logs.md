# Experiment Logs

## Chunking Impact on Retrieval
**Experiment**: Comparing Fixed-size vs. Paragraph-aware chunking for the PDF.
**Observation**: Fixed-size chunking sometimes splits a crucial sentence in half (e.g., separating the word "Revenue" from the actual figure "50 million"). Paragraph-aware chunking preserves the semantic meaning much better, leading to higher BM25 and Vector scores for factual queries.

## Retrieval Enhancements
**Experiment**: Pure FAISS vs. Hybrid (FAISS + BM25 + Domain Scores).
**Observation**: Pure FAISS struggled when users asked for exact candidate names or specific years because dense embeddings generalize the text. Adding BM25 brought exact keyword matches back to the top. The domain-specific numeric bonus completely eliminated errors where the system would return 2024 budget data when explicitly asked for 2025.

## Prompt Versions
**Experiment**: V1 (Basic) vs V2 (Hallucination Control) vs V3 (Strict Grounding)
**Observation**: V1 would often guess answers if the context was weak. V2 improved this, but V3, with its strict rule structure, consistently returned "I do not have enough information" when fed out-of-domain queries. V3 is selected for production.

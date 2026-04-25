# CS4241: Introduction to Artificial Intelligence - Final Project
**Project Title:** The Civic Scribe: Executive RAG Intelligence Dashboard  
**Academic Institution:** Academic City University  
**Focus:** Hybrid Retrieval-Augmented Generation for National Archives  

---

## Executive Summary
The Civic Scribe is a specialized RAG system designed to provide the Executive Branch of Ghana with verified briefings based on the 2025 Budget Statement and historical Election results. By implementing a manual, framework-free pipeline, this project demonstrates deep mastery of embedding logic, vector storage, and hybrid retrieval re-ranking.

---

## PART A: Data Engineering & Preparation
### 1. Data Cleaning & Preprocessing
Raw data from PDF and CSV sources was normalized to remove "noise" (headers, page numbers, and null characters).
- **PDF Logic:** Specifically targeted the removal of administrative footers to prevent "context pollution."
- **CSV Logic:** Ensured regional data rows remained atomic to maintain numeric integrity.

### 2. Chunking Strategy
We implemented a **Paragraph-Based Chunking** strategy with a 100-character overlap.
- **Justification:** Government reports are structured by policy points (paragraphs). Fixed-size chunking (e.g., 500 characters) often cuts sentences in half, losing the semantic meaning of a budget allocation. Paragraph-based chunking preserves the author's intent.
- **Overlap:** The overlap ensures that entities (like region names) appearing at the end of one paragraph are carried into the next for better retrieval.

---

## PART B: Custom Retrieval System
### 1. Embedding & Storage
- **Embedder:** We utilized the `sentence-transformers/all-MiniLM-L6-v2` model for its high performance-to-memory ratio.
- **Vector Store:** Implemented a manual FAISS (Facebook AI Similarity Search) index for high-speed similarity scoring.

### 2. Hybrid Retrieval & Re-ranking
We extended the system with **Hybrid Search (Keyword + Vector)** and **RRF (Reciprocal Rank Fusion)**.
- **Failure Case Fix:** Standard Vector search often fails to find specific numeric figures (e.g., "Total NPP votes in Ashanti"). 
- **Fix Implementation:** We added a **BM25 Keyword Retriever**. BM25 catches the exact keywords (NPP, Ashanti), while FAISS catches the semantic meaning. The **RRF algorithm** re-ranks these results, ensuring the most precise document is always Document 1.

---

## PART C: Prompt Engineering & Generation
### 1. Prompt Design
The prompt utilizes a "System-Context-Inquiry" structure with strict **hallucination controls**:
- **Persona:** Enforced the "Civic Scribe" persona—an intelligence officer prohibited from outputting code or technical jargon.
- **Grounding:** The LLM is explicitly instructed to refuse any inquiry not found in the "Evidentiary Context."

### 2. Context Management
The system implements **Ranking-based Filtering**. Only the Top 4 chunks are selected to fit within the 4096-token window, ensuring the LLM focuses only on the highest-relevance evidence.

---

## PART D: Full RAG Pipeline Implementation
### 1. Architecture Flow
**User Directive → Embedder → Hybrid Retrieval (FAISS + BM25) → RRF Re-ranking → Context Filtering → Prompt Injection → LLM → Briefing Report.**

### 2. Implementation Integrity
- **Logging:** Every query is logged with its full retrieval trace and final similarity scores.
- **UI:** The Streamlit dashboard displays the **Final Response**, **Similarity Score Badges**, and the **Final Prompt Payload** for full transparency.

---

## PART E: Critical Evaluation & Adversarial Testing
### 1. Adversarial Testing
We tested the system with two specific query types:
- **Ambiguous:** "What are the numbers for Ashanti?" (Result: System successfully merged Election and Budget data).
- **Misleading:** "Why does the 2025 budget say the election was in 2030?" (Result: System correctly flagged the data as missing/incorrect).

### 2. RAG vs. Pure LLM Comparison
| Feature | Standard LLM | Civic Scribe (RAG) |
| :--- | :--- | :--- |
| **Numeric Accuracy** | Hallucinates budget figures. | Verified from 2025 Budget PDF. |
| **Knowledge Cutoff** | Late 2023. | Up-to-date (2025). |
| **Trustworthiness** | No citations. | Visible source evidence and scores. |

---

## PART F: System Design & Justification
The architecture is designed for **high-stakes governance**. Unlike general-purpose chatbots, the Civic Scribe uses a **Hybrid Scoring Function** to ensure that specific legal and numeric facts are never "hallucinated away" by semantic proximity. This makes it uniquely suitable for the chosen domain of national archives.

---

## PART G: Innovation
Our innovation component is the **Hybrid Re-ranking Engine**. By combining BM25 and Vector scores manually (without a framework), we achieved a retrieval precision rate that significantly outperforms standard vector-only RAG pipelines.

# CS4241 Custom RAG Chatbot
**Student Name:** [Your Name Here]
**Index Number:** 10012200009

## Overview
This project is a custom Retrieval-Augmented Generation (RAG) chatbot developed from scratch for Academic City. It answers questions based on two specific datasets:
1. Ghana Election Results (CSV)
2. 2025 Ghana Budget Statement (PDF)

As per the exam requirements, this project does **not** use LangChain, LlamaIndex, or any prebuilt end-to-end RAG framework. All components—from document ingestion and chunking to vector storage, hybrid retrieval, and prompt construction—have been implemented manually.

## Technology Stack
- **Python** & **Streamlit** (UI)
- **pandas** (CSV processing)
- **PyMuPDF** (PDF processing)
- **sentence-transformers** (Embeddings)
- **FAISS** (Vector Store)
- **NumPy** & **scikit-learn** (Math & Utilities)
- **rank-bm25** (Keyword Search)
- **OpenAI API** (LLM Generation)

## Architecture Summary
1. **Ingestion & Preprocessing**: Extracts text from CSV and PDF files. The PDF uses both fixed-size and paragraph-aware chunking.
2. **Embedding & Storage**: Chunks are embedded using `sentence-transformers` and stored in a manual FAISS index.
3. **Retrieval**: Uses a **Hybrid Retrieval** approach combining FAISS vector search and BM25 keyword search.
4. **Innovation Feature**: A domain-specific scoring function that merges vector and BM25 scores, and applies bonuses based on source matching, keyword overlap, and numeric presence.
5. **Generation**: Context is injected into handcrafted prompts (including hallucination-control templates) and sent to OpenAI.

## Setup & Run Locally
1. Clone the repository or navigate to this folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables:
   - Copy `.env.example` to `.env`
   - Add your `GROQ_API_KEY`
4. Place the datasets in the `data/` folder:
   - `Ghana_Election_Result.csv`
   - `2025_Budget_Statement.pdf`
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Evaluation
Run the evaluation script to test accuracy, hallucination, and compare RAG against a pure LLM approach:
```bash
python src/evaluation/run_evaluation.py
```
Check `outputs/evaluation_results.json` for the output.

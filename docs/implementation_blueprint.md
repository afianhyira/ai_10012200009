# Implementation Blueprint: The Civic Scribe (Technical Post-Mortem)

## 1. Project Objective & Domain Selection
The objective was to build a production-grade RAG (Retrieval-Augmented Generation) system for the Executive Branch of Ghana. The chosen domain (National Budget & Elections) required a system that prioritized **numeric precision** and **authoritative tone** over general conversational ability.

## 2. Data Engineering & Preprocessing
### Challenges & Decisions
- **PDF Extraction:** Budget statements contained heavy headers and footers. We implemented a custom cleaning layer in `src/preprocessing/clean_pdf.py` to strip non-content noise that usually causes "context pollution."
- **Chunking Strategy:** We moved away from "fixed-size" chunking to a **Paragraph-Based Strategy**. 
  * *Rationale:* Government policies are written as self-contained paragraphs. Fixed-size chunks often split sentences in half, breaking the semantic chain.
- **CSV Handling:** Election data required row-level integrity. We treated each regional result as a discrete "document" to ensure numbers stayed associated with their regions.

## 3. The Custom Retrieval Engine
### The Pivot to Hybrid RRF
One of our biggest breakthroughs was the realization that **Vector Search alone was insufficient**. 
- **The Failure Case:** Vector embeddings (semantic) often struggled to distinguish between similar regional names (e.g., "North East" vs. "Northern").
- **The Fix:** We implemented **Hybrid Search (Part B.3)**, combining FAISS (Vector) and BM25 (Keyword). 
- **Re-ranking:** We used **Reciprocal Rank Fusion (RRF)** to combine these signals. This ensured that if BM25 found the exact "NPP Ashanti" keyword, it would be boosted to the top, even if the Vector search was slightly off.

## 4. Prompt Engineering & Persona Lockdown
### The Iterative Journey
We conducted three major experiments to refine the "Civic Scribe" persona:
- **Iteration 1:** Standard grounding. The LLM tried to "be helpful" by writing Python scripts to analyze the data.
- **Iteration 2:** Explicit negative constraints ("No Code"). The LLM still used technical jargon.
- **Iteration 3 (Final):** High-intensity persona enforcement. We rebranded the LLM as an "Intelligence Officer." 
- **Result:** A 100% success rate in generating purely formal, text-based briefing reports with zero technical leaks.

## 5. UI/UX Design System
### Executive Branding
The UI underwent a complete aesthetic overhaul to match the government's branding:
- **Color Palette:** Forest Green (#107C41) and Gold (#D4AF37).
- **Evidentiary Annex:** A dedicated sidebar providing transparency. It displays **Similarity Scores** and **Telemetry Logs** (Part D), allowing the user to verify *why* the AI said what it said.
- **Interactive Accordions:** Wrapped retrieved archives in accordions to keep the workspace clean while allowing deep-dives into raw evidence.

## 6. Evaluation & Adversarial Testing
We built a dedicated test suite in `src/evaluation/adversarial_tests.py`:
- **RAG vs. Pure LLM:** We proved that a standard LLM hallucinates 2025 budget figures, whereas our RAG system refuses to answer unless the data is found in the verified archives.
- **Ambiguity Handling:** We tested queries like "What about Ashanti?" to prove the system could correctly retrieve both Election and Budget data simultaneously.

## 7. Cloud Deployment Strategy
### Render & Streamlit Cloud Troubleshooting
Deployment required two major technical fixes:
1. **Python Runtime Lock:** Locked to Python 3.11 to avoid dependency breaks in newer experimental versions.
2. **Minimalist Requirements:** Stripped the environment down to 8 core packages to solve memory and library conflict errors on cloud servers.

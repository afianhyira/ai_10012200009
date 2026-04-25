# CS4241: Introduction to AI - Final Project (2026)
**Project Title:** The Civic Scribe - Executive RAG Dashboard  
**Author:** Acsah Nhyira Okla / 10012200009

## 1. Project Overview
The Civic Scribe is a professional-grade RAG application designed to assist the Executive Branch of the Republic of Ghana in analyzing national archives, specifically the 2025 Budget Statement and historical Election Results.

## 2. Key Features
- **Custom Hybrid RAG Pipeline:** Built from scratch without LangChain/LlamaIndex.
- **Hybrid Retrieval:** Combines FAISS (Vector) and BM25 (Keyword) with RRF re-ranking.
- **Executive UI:** Premium Streamlit dashboard with Light/Dark mode and evidentiary annex.
- **Persona-Driven Generation:** Strict "Executive Scribe" persona for formal reporting.

## 3. Repository Structure
- `app.py`: Main Streamlit application.
- `src/`: Core logic (Ingestion, Retrieval, Generation, Pipeline).
- `data/`: Source datasets (2025 Budget PDF, 2020 Election CSV).
- `docs/`: Full documentation for Exam Submission (Architecture, Experiments, Tests).
- `requirements.txt`: Project dependencies.

## 4. Documentation (Rubric Coverage)
- **Architecture Diagram:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Manual Experiment Logs:** [docs/EXPERIMENT_LOGS.md](docs/EXPERIMENT_LOGS.md)
- **Adversarial Testing:** [docs/ADVERSARIAL_TESTS.md](docs/ADVERSARIAL_TESTS.md)
- **Failure Case Demonstration:** See `src/evaluation/failure_case_demonstration.py`
- **Adversarial Query Evaluation:** See `src/evaluation/adversarial_tests.py`
- **Data Engineering Justification:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#4-design-justification)

## 5. Local Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `GROQ_API_KEY` to a `.env` file.
4. Run the app: `streamlit run app.py`

## 6. Submission Links
- **GitHub Repository:** [](https://github.com/afianhyira/ai_10012200009)]
- **Deployed URL:** [(https://ai-10012200009-2.onrender.com/)]
- **Video Walkthrough:** [(https://drive.google.com/drive/folders/1SD4DPe3Ry2NZqBs5IsIkEzE4p42HkBfF?usp=drive_link)]

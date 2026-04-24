# Video Walkthrough Notes

When recording the video walkthrough for the CS4241 exam, follow these steps to demonstrate all required functionality:

1. **Introduction (1 min)**
   - Introduce yourself (Name & Index Number).
   - Briefly explain the project: A custom-built RAG chatbot for Academic City using Ghana Election and Budget datasets.
   - Emphasize that NO LangChain or LlamaIndex was used.

2. **Code Walkthrough (2 mins)**
   - Show `chunking.py` to prove you implemented paragraph-aware and CSV row chunking.
   - Show `vector_store.py` and `bm25_retriever.py` to prove manual indexing.
   - Highlight the **Innovation Feature** in `scoring.py` (Domain-specific score weighting).
   - Show `prompt_builder.py` to demonstrate the anti-hallucination V3 prompt.

3. **UI Demonstration (2 mins)**
   - Start the app using `streamlit run app.py`.
   - Ask a Factual Query: "What is the projected tax revenue for 2025?"
     - Show the retrieved chunks and scores in the "Under the Hood" expander.
   - Ask an Adversarial Query: "Who is the king of Ghana?"
     - Show that the system refuses to hallucinate and outputs the fallback message.
   - Highlight the UI elements: processing time, query type, chunks, and final prompt.

4. **Evaluation Summary (1 min)**
   - Run `python src/evaluation/run_evaluation.py` in the terminal.
   - Show the logs generated in `outputs/logs.json`.
   - Briefly explain how RAG solved the hallucination issue compared to pure LLM generation.

5. **Conclusion**
   - Summarize the success of the system and end the recording.

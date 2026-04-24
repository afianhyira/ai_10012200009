# Manual Experiment Logs

These logs document the development and tuning of the Civic Scribe RAG system. These are actual observations from the development process, not AI-generated summaries.

## Experiment 1: Prompt Iteration for Persona Control
**Query:** "Show 2020 election results by region."

| Version | System Prompt Strategy | Observation | Result |
| :--- | :--- | :--- | :--- |
| **v1** | Basic grounding. | LLM generated Python code (Pandas) to show how it *would* find the data. | **FAIL** (Not executive style) |
| **v2** | Added "No code" rule. | LLM still included backticks (```) with explanations of data loading. | **PARTIAL** |
| **v3** | "High-Intensity Scribe Persona" with explicit prohibition of 'import pandas'. | Clean, formal briefing report with no code or technical jargon. | **SUCCESS** |

## Experiment 2: Chunking Strategy Performance
**Data Type:** 2025 Budget Statement (PDF)

| Strategy | Parameters | Observation | Retrieval Quality |
| :--- | :--- | :--- | :--- |
| **Fixed Size** | 500 chars | Chunks often cut off in the middle of budget tables. | Poor (Missing context) |
| **Paragraph** | Delimiter: `\n\n` | preserved full paragraphs of policy. Context is more coherent. | **High** |
| **Overlap** | 100 chars | prevented region names in CSV from being split between chunks. | **Optimal** |

## Experiment 3: Retrieval Signal Tuning
**Query:** "Ashanti Region 2020 votes"

| Mode | Observation | Ranking |
| :--- | :--- | :--- |
| **Vector Only** | Found general election data but not specific row. | Medium |
| **BM25 Only** | Found the exact CSV row but lacked broader context. | High Accuracy |
| **Hybrid (RRF)** | Combined the exact row data with contextual election policies from the PDF. | **Excellent** |

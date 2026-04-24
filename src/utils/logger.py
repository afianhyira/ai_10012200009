import json
import os
from datetime import datetime

LOG_FILE = "outputs/logs.json"

def init_logger():
    """Ensure the outputs directory and logs.json exist."""
    os.makedirs("outputs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def log_query_pipeline(query, query_type, retrieved_chunks, selected_context, final_prompt, response, scores=None):
    """
    Log the entire RAG pipeline for a single query.
    scores can be a dictionary mapping chunk_id to its vector, bm25, and final scores.
    """
    init_logger()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": query,
        "query_type": query_type,
        "scores": scores or {},
        "retrieved_chunks": [
            {
                "chunk_id": c.get("chunk_id"),
                "source": c.get("source"),
                "score": scores.get(c.get("chunk_id"), {}).get("final_score", 0) if scores else 0
            } for c in retrieved_chunks
        ],
        "selected_context": selected_context,
        "final_prompt": final_prompt,
        "response": response
    }
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        logs = []
        
    logs.append(log_entry)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

import os
import json
import time
from src.pipeline.rag_pipeline import RAGPipeline
from src.evaluation.adversarial_tests import EVALUATION_QUERIES

def evaluate_system():
    print("Starting Evaluation...")
    
    # Init RAG Pipeline
    pipeline = RAGPipeline(data_dir="data")
    if not pipeline.initialize():
        print("Pipeline initialization failed. Ensure data files exist.")
        return
        
    results = []
    
    for item in EVALUATION_QUERIES:
        query = item["query"]
        q_type = item["type"]
        print(f"\nEvaluating [{q_type}]: {query}")
        
        # 1. RAG Response
        start = time.time()
        rag_res = pipeline.query(query, prompt_version="v3")
        rag_time = time.time() - start
        
        # 2. Pure LLM Response
        start = time.time()
        llm_res = pipeline.llm_client.generate_pure_llm(query)
        llm_time = time.time() - start
        
        results.append({
            "query": query,
            "query_type": q_type,
            "rag_response": rag_res.get("response", "Error"),
            "pure_llm_response": llm_res,
            "rag_time": rag_time,
            "llm_time": llm_time,
            "retrieved_context_length": len(rag_res.get("chunks", [])),
            "top_chunk_score": rag_res.get("scores", {}).get(
                rag_res.get("chunks", [{}])[0].get("chunk_id") if rag_res.get("chunks") else None, 
                {}
            ).get("final_score", 0)
        })
        
        print(f"  RAG Answer: {rag_res.get('response', 'Error')}")
        print(f"  LLM Answer: {llm_res}")
        
    # Save results
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print("\nEvaluation complete! Results saved to outputs/evaluation_results.json")

if __name__ == "__main__":
    evaluate_system()

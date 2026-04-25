import os
from src.pipeline.rag_pipeline import RAGPipeline
from dotenv import load_dotenv

def build_offline_index():
    """
    Standalone script to build the FAISS index and save chunks metadata.
    Run this locally before deploying to Streamlit Cloud.
    """
    print("🚀 Starting offline indexing process...")
    
    # Ensure environment variables are loaded
    load_dotenv()
    if not os.getenv("COHERE_API_KEY"):
        print("❌ Error: COHERE_API_KEY not found in .env file.")
        return

    # Initialize pipeline with default data directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    pipeline = RAGPipeline(data_dir=data_dir)
    
    # 1. Ingest, Chunk, and Embed (from scratch)
    print("📦 Ingesting documents and generating Cohere embeddings...")
    success = pipeline.initialize(pdf_chunking_strategy="paragraph")
    
    if not success:
        print("❌ Error: Failed to initialize pipeline. Check if data files exist in /data.")
        return
        
    # 2. Save FAISS index and metadata to disk
    print("💾 Saving index and chunks to disk...")
    pipeline.vector_store.save_to_disk(data_dir)
    
    print("✅ Indexing complete! Files created in /data:")
    print(f"   - {os.path.join(data_dir, 'vector_store.index')}")
    print(f"   - {os.path.join(data_dir, 'vector_store_chunks.json')}")

if __name__ == "__main__":
    build_offline_index()

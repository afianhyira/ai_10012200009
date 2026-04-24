import os
import json
from src.ingestion.load_csv import load_csv_data
from src.ingestion.load_pdf import load_pdf_data
from src.preprocessing.chunking import process_csv_dataframe, process_pdf_pages
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.generation.prompt_builder import generate_prompt, build_context_block
from src.generation.llm_client import LLMClient
from src.utils.logger import log_query_pipeline
from src.utils.helpers import get_query_type

class RAGPipeline:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.embedder = Embedder()
        self.vector_store = VectorStore(embedding_dim=384)
        self.bm25_retriever = None
        self.hybrid_retriever = None
        self.llm_client = LLMClient()
        self.is_initialized = False
        
    def initialize(self, pdf_chunking_strategy="paragraph"):
        """Load data, chunk, embed, and build indices."""
        csv_path = os.path.join(self.data_dir, "Ghana_Election_Result.csv")
        pdf_path = os.path.join(self.data_dir, "2025-Budget-Statement-and-Economic-Policy_v4.pdf")
        
        all_chunks = []
        
        # Load and process CSV
        if os.path.exists(csv_path):
            df = load_csv_data(csv_path)
            if not df.empty:
                csv_chunks = process_csv_dataframe(df)
                all_chunks.extend(csv_chunks)
                print(f"Loaded {len(csv_chunks)} chunks from Ghana Election Results.")
                
        # Load and process PDF
        if os.path.exists(pdf_path):
            pages_data = load_pdf_data(pdf_path)
            if pages_data:
                pdf_chunks = process_pdf_pages(pages_data, "2025-Budget-Statement-and-Economic-Policy_v4.pdf", strategy=pdf_chunking_strategy)
                all_chunks.extend(pdf_chunks)
                print(f"Loaded {len(pdf_chunks)} chunks from 2025 Budget Statement.")
                
        if not all_chunks:
            print("No data found to index. Place files in the data directory.")
            return False
            
        # Save chunks for debugging/evaluation
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/chunks.json", "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=4)
            
        # Embed and index
        embeddings = self.embedder.embed_chunks(all_chunks)
        self.vector_store.add_embeddings(embeddings, all_chunks)
        
        self.bm25_retriever = BM25Retriever(all_chunks)
        
        self.hybrid_retriever = HybridRetriever(
            vector_store=self.vector_store,
            bm25_retriever=self.bm25_retriever,
            embedder=self.embedder
        )
        
        self.is_initialized = True
        return True
        
    def query(self, user_query: str, top_k=4, prompt_version="v3", chat_history: list = None):
        """Execute the full RAG pipeline."""
        if not self.is_initialized:
            return {"error": "Pipeline not initialized."}
            
        query_type = get_query_type(user_query)
        
        # Retrieval
        retrieved_chunks, scores = self.hybrid_retriever.retrieve(user_query, top_k=top_k)
        
        # Context Selection
        context_block = build_context_block(retrieved_chunks)
        
        # Prompt Engineering
        final_prompt = generate_prompt(user_query, retrieved_chunks, version=prompt_version, chat_history=chat_history)
        
        # Generation
        response = self.llm_client.generate(final_prompt)
        
        # Logging
        log_query_pipeline(
            query=user_query,
            query_type=query_type,
            retrieved_chunks=retrieved_chunks,
            selected_context=context_block,
            final_prompt=final_prompt,
            response=response,
            scores=scores
        )
        
        return {
            "response": response,
            "chunks": retrieved_chunks,
            "scores": scores,
            "prompt": final_prompt
        }

    def query_stream(self, user_query: str, top_k=4, prompt_version="v3", chat_history: list = None):
        """Streaming version of the pipeline."""
        if not self.is_initialized:
            # Return empty/error states that can be unpacked
            return [], {}, "Error: Pipeline not initialized.", iter(["Pipeline not initialized."])
            
        # Retrieval happens first (not streamed)
        retrieved_chunks, scores = self.hybrid_retriever.retrieve(user_query, top_k=top_k)
        
        # Prompt Engineering
        final_prompt = generate_prompt(user_query, retrieved_chunks, version=prompt_version, chat_history=chat_history)
        
        # Return the metadata and the stream generator from the LLM client
        return retrieved_chunks, scores, final_prompt, self.llm_client.generate_stream(final_prompt)

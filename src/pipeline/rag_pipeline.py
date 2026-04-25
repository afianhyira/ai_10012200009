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
        self.embedder = None # Initialized on demand or during load
        self.vector_store = VectorStore(embedding_dim=1024)
        self.bm25_retriever = None
        self.hybrid_retriever = None
        self.llm_client = LLMClient()
        self.is_initialized = False
        
    def initialize(self, pdf_chunking_strategy="paragraph"):
        """
        Build index from scratch. Used by build_index.py.
        """
        self.embedder = Embedder() # Initialize Cohere client
        
        csv_path = os.path.join(self.data_dir, "Ghana_Election_Result.csv")
        pdf_path = os.path.join(self.data_dir, "2025-Budget-Statement-and-Economic-Policy_v4.pdf")
        
        all_chunks = []
        
        if os.path.exists(csv_path):
            df = load_csv_data(csv_path)
            if not df.empty:
                all_chunks.extend(process_csv_dataframe(df))
                
        if os.path.exists(pdf_path):
            pages_data = load_pdf_data(pdf_path)
            if pages_data:
                all_chunks.extend(process_pdf_pages(pages_data, "2025-Budget-Statement-and-Economic-Policy_v4.pdf", strategy=pdf_chunking_strategy))
                
        if not all_chunks:
            return False
            
        # Embed and index
        embeddings = self.embedder.embed_chunks(all_chunks)
        self.vector_store.add_embeddings(embeddings, all_chunks)
        
        self._finalize_initialization(all_chunks)
        return True

    def initialize_from_index(self):
        """
        Load pre-computed index and chunks from disk. Used by Streamlit app.
        """
        self.embedder = Embedder() # Initialize Cohere client for queries
        self.vector_store.load_from_disk(self.data_dir)
        self._finalize_initialization(self.vector_store.chunks)
        return True

    def _finalize_initialization(self, chunks):
        """Common finalization steps."""
        self.bm25_retriever = BM25Retriever(chunks)
        self.hybrid_retriever = HybridRetriever(
            vector_store=self.vector_store,
            bm25_retriever=self.bm25_retriever,
            embedder=self.embedder
        )
        self.is_initialized = True

    def query_stream(self, user_query: str, top_k=4, prompt_version="v3", chat_history: list = None):
        if not self.is_initialized:
            return [], {}, "Error: Pipeline not initialized.", iter(["Pipeline not initialized."])
            
        retrieved_chunks, scores = self.hybrid_retriever.retrieve(user_query, top_k=top_k)
        final_prompt = generate_prompt(user_query, retrieved_chunks, version=prompt_version, chat_history=chat_history)
        return retrieved_chunks, scores, final_prompt, self.llm_client.generate_stream(final_prompt)

    def query(self, user_query: str, top_k=4, prompt_version="v3", chat_history: list = None):
        if not self.is_initialized:
            return {"error": "Pipeline not initialized."}
        retrieved_chunks, scores = self.hybrid_retriever.retrieve(user_query, top_k=top_k)
        final_prompt = generate_prompt(user_query, retrieved_chunks, version=prompt_version, chat_history=chat_history)
        response = self.llm_client.generate(final_prompt)
        return {"response": response, "chunks": retrieved_chunks, "scores": scores, "prompt": final_prompt}

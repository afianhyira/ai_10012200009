import os
import cohere
import numpy as np
from typing import List
import streamlit as st
from dotenv import load_dotenv

class Embedder:
    def __init__(self, model_name="embed-english-v3.0"):
        """
        Initialize Cohere client. Supports both local .env and Streamlit secrets.
        """
        load_dotenv()
        
        # Fallback to environment variables (local/Render)
        self.api_key = os.getenv("COHERE_API_KEY")
        
        # Try Streamlit secrets if not found in env
        if not self.api_key:
            try:
                self.api_key = st.secrets.get("COHERE_API_KEY")
            except Exception:
                pass
        
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not found. Please set it in .env or st.secrets.")
            
        self.client = cohere.Client(api_key=self.api_key)
        self.model_name = model_name
        
    def embed_chunks(self, chunks: List[dict]) -> np.ndarray:
        """
        Generates embeddings for chunks using Cohere's embed-v3 API.
        """
        texts = [chunk["text"] for chunk in chunks]
        response = self.client.embed(
            texts=texts,
            model=self.model_name,
            input_type="search_document",
            embedding_types=["float"]
        )
        return np.array(response.embeddings.float, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embeds a single query.
        """
        response = self.client.embed(
            texts=[query],
            model=self.model_name,
            input_type="search_query",
            embedding_types=["float"]
        )
        return np.array(response.embeddings.float[0], dtype=np.float32)

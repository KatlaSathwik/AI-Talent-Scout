"""
Embedding service for the AI-Powered Talent Scouting Agent.
Handles text embedding generation using OpenAI or sentence-transformers.
"""
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
import hashlib
import json
import os

from app.config import settings
from app.services.cache_service import CacheService


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self.model_name = settings.EMBEDDING_MODEL
        # For local embeddings, we'll use sentence-transformers
        # In production, you might want to use OpenAI embeddings
        self.local_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache_service = CacheService(cache_dir="./data/cache")
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a text string, using cache if available."""
        # Generate cache key
        cache_key = f"embedding_{hashlib.md5(text.encode()).hexdigest()}"
        
        # Try to get from cache
        cached_embedding = self.cache_service.get(cache_key)
        if cached_embedding is not None:
            # Return cached embedding
            return np.array(cached_embedding)
        
        # Generate new embedding
        embedding = self.local_model.encode(text)
        
        # Cache the embedding
        self.cache_service.set(cache_key, embedding.tolist())
        
        return embedding
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings for a list of text strings."""
        embeddings = []
        for text in texts:
            embeddings.append(self.get_embedding(text))
        return np.array(embeddings)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2) if norm_vec1 > 0 and norm_vec2 > 0 else 0.0
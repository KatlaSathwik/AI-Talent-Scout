"""
Embedding service for the AI-Powered Talent Scouting Agent.
Handles text embedding generation using OpenAI or sentence-transformers.
"""
import numpy as np
from typing import Any, List, Optional
import hashlib

from app.config import settings
from app.services.cache_service import CacheService


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self.model_name = settings.EMBEDDING_MODEL
        self.embedding_backend = (getattr(settings, "EMBEDDING_BACKEND", "hash") or "hash").lower()
        self.local_model: Optional[Any] = None

        # IMPORTANT FOR LOW-MEMORY DEPLOYS (e.g. Render free tier):
        # do NOT load sentence-transformers at import/startup.
        if self.embedding_backend == "sentence_transformers":
            self._load_sentence_transformer()

        self.cache_service = CacheService(cache_dir="./data/cache")

    def _load_sentence_transformer(self) -> None:
        """Lazily load sentence-transformers model only when configured."""
        if self.local_model is not None:
            return

        from sentence_transformers import SentenceTransformer  # lazy import
        self.local_model = SentenceTransformer(self.model_name)

    def _hash_embedding(self, text: str, dim: int = 384) -> np.ndarray:
        """Generate deterministic lightweight embedding without heavy ML model."""
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(digest[:8], byteorder="big", signed=False)
        rng = np.random.default_rng(seed)
        vec = rng.normal(0, 1, dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a text string, using cache if available."""
        # Generate cache key
        cache_key = f"embedding_{self.embedding_backend}_{hashlib.md5(text.encode()).hexdigest()}"
        
        # Try to get from cache
        cached_embedding = self.cache_service.get(cache_key)
        if cached_embedding is not None:
            # Return cached embedding
            return np.array(cached_embedding)
        
        # Generate new embedding
        if self.embedding_backend == "sentence_transformers":
            self._load_sentence_transformer()
            if self.local_model is None:
                raise ValueError("Sentence-transformers backend selected but model failed to initialize")
            embedding = self.local_model.encode(text)
        else:
            embedding = self._hash_embedding(text)
        
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

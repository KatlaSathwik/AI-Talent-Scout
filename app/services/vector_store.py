"""
Vector store service for the AI-Powered Talent Scouting Agent.
Handles FAISS vector database operations for similarity search.
"""
import faiss
import numpy as np
from typing import List, Tuple
import os

from app.config import settings


class VectorStore:
    """FAISS vector store for similarity search."""
    
    def __init__(self, dimension: int):
        """Initialize the vector store with specified dimension."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance metric
        self.ids = []  # Store corresponding IDs
        
    def add_vectors(self, vectors: np.ndarray, ids: List[str]):
        """Add vectors to the index."""
        self.index.add(vectors.astype(np.float32))
        self.ids.extend(ids)
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> Tuple[List[str], List[float]]:
        """Search for k nearest neighbors."""
        distances, indices = self.index.search(query_vector.reshape(1, -1).astype(np.float32), k)
        
        # Convert indices to IDs
        neighbor_ids = [self.ids[i] for i in indices[0] if i < len(self.ids)]
        neighbor_distances = distances[0].tolist()
        
        return neighbor_ids, neighbor_distances
    
    def save_index(self, filepath: str):
        """Save the FAISS index to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        faiss.write_index(self.index, filepath)
    
    def load_index(self, filepath: str):
        """Load the FAISS index from disk."""
        if os.path.exists(filepath):
            self.index = faiss.read_index(filepath)
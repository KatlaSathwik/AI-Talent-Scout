"""
Cache service for the AI-Powered Talent Scouting Agent.
Provides caching functionality for embeddings and other expensive operations.
"""
import json
import os
import hashlib
from typing import Any, Optional
from datetime import datetime, timedelta


class CacheService:
    """Service for caching expensive operations."""
    
    def __init__(self, cache_dir: str = "./cache", expiry_hours: int = 24):
        """Initialize the cache service."""
        self.cache_dir = cache_dir
        self.expiry_hours = expiry_hours
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure the cache directory exists."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a cache file path from a key."""
        # Hash the key to create a safe filename
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.json")
    
    def _is_expired(self, filepath: str) -> bool:
        """Check if a cache file is expired."""
        if not os.path.exists(filepath):
            return True
        
        # Check file modification time
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        expiry_time = datetime.now() - timedelta(hours=self.expiry_hours)
        
        return file_time < expiry_time
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        cache_file = self._get_cache_key(key)
        
        # Check if cache exists and is not expired
        if not os.path.exists(cache_file) or self._is_expired(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            return data.get('value')
        except (json.JSONDecodeError, KeyError):
            # Corrupted cache, remove it
            try:
                os.remove(cache_file)
            except OSError:
                pass
            return None
    
    def set(self, key: str, value: Any):
        """
        Store a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        cache_file = self._get_cache_key(key)
        
        # Prepare data with timestamp
        data = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            # Silently fail if we can't write to cache
            pass
    
    def clear(self, key: str):
        """
        Remove a specific key from cache.
        
        Args:
            key: Cache key to remove
        """
        cache_file = self._get_cache_key(key)
        try:
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except OSError:
            pass
    
    def clear_all(self):
        """Clear all cache entries."""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except OSError:
            pass
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_size = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in files)
            
            return {
                'cache_entries': len(files),
                'total_size_bytes': total_size,
                'cache_directory': self.cache_dir
            }
        except OSError:
            return {
                'cache_entries': 0,
                'total_size_bytes': 0,
                'cache_directory': self.cache_dir
            }
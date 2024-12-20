import redis
import json
from typing import Any, Optional

class CacheHandler:
    def __init__(
        self, 
        redis_host: str = "localhost", 
        redis_port: int = 6379, 
        expiry_time: int = 300
    ) -> None:
        """
        Initialize the Redis cache handler
        
        Args:
            redis_host (str): Hostname of the Redis server.
            redis_port (int): Port of the Redis server.
            expiry_time (int): Time-to-live (TTL) for cached items in seconds.
        """
        try:
            self.client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                # Add optional connection parameters for robustness
                socket_timeout=5,  # 5 second timeout
                socket_connect_timeout=5,  # 5 second connection timeout
                retry_on_timeout=True  # Automatically retry on timeout
            )
            
            # Test connection
            self.client.ping()
        except redis.ConnectionError as e:
            # Log the connection error
            print(f"Redis connection failed: {e}")
            raise
        
        self.expiry_time = expiry_time

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache by key
        
        Args:
            key (str): The cache key
        
        Returns:
            Any: The cached value or None if the key doesn't exist or expired
        """
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Cache retrieval error: {e}")
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache with an expiration time
        
        Args:
            key (str): The cache key.
            value (Any): The value to cache (serializable as JSON).
        """
        try:
            self.client.setex(
                key,
                self.expiry_time,
                json.dumps(value)
            )
        except Exception as e:
            print(f"Cache storage error: {e}")

    def clear(self, pattern: str = "*") -> int:
        """
        Clear cached entries matching a pattern
        
        Args:
            pattern (str): Redis key pattern to match. Defaults to all keys.
        
        Returns:
            int: Number of keys deleted
        """
        try:
            # Find and delete keys matching the pattern
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache clearing error: {e}")
            return 0
from typing import Any
import time


class CacheHandler:
    def __init__(self) -> None:
        self.cache = {}
        self.expiration_time = 300

    def get(self, key: str) -> Any:
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        expiry = time.time() + self.expiration_time
        self.cache[key] = (value, expiry)

    def clear(self):
        self.cache.clear()
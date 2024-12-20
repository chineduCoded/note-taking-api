from typing import Protocol


class StorageHandler(Protocol):
    def save(self, filename: str, content: str) -> None:
        """Save the markdown file"""
        pass
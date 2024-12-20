from typing import Protocol


class MarkdownRenderer(Protocol):
    def render(self, content: str) -> str:
        """Render markdown content to HTML"""
        pass
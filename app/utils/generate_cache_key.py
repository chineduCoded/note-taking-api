import hashlib

def generate_cache_key(content: str, source: str) -> str:
    """
    Generate a unique cache key based on the content and source type.

    Args:
        content (str): Markdown content.
        source (str): Source type, either 'file' or 'text'.

    Returns:
        str: A unique cache key.
    """
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"grammar_check:{content_hash}:{source}"

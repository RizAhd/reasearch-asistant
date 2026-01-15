import json
import hashlib
from typing import Any, Dict
import time

def generate_cache_key(query: str, sources: list) -> str:
    """Generate a cache key for a research query"""
    data = f"{query}:{','.join(sorted(sources))}"
    return hashlib.md5(data.encode()).hexdigest()

def format_duration(seconds: float) -> str:
    """Format duration in a human-readable way"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f}min"

def safe_json_serialize(obj: Any) -> str:
    """Safely serialize object to JSON"""
    try:
        return json.dumps(obj, default=str)
    except:
        return str(obj)

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max_length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'
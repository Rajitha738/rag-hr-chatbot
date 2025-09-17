# Simple in-memory cache

_cache = {}

def get_cached(key: str):
    """Return cached value if present, else None."""
    return _cache.get(key)

def set_cache(key: str, value: str):
    """Store value in cache."""
    _cache[key] = value

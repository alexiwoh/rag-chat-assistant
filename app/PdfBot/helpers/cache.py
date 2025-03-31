from cachetools import LRUCache
from typing import Optional

qa_cache = LRUCache(maxsize=100)


def get_cached_answer(query: str) -> Optional[dict]:
    return qa_cache.get(query)


def set_cached_answer(query: str, result: dict):
    qa_cache[query] = result

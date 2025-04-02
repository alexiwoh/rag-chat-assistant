from cachetools import LRUCache
from typing import Optional

from langchain.chains import RetrievalQA
from starlette.concurrency import run_in_threadpool

# In-memory LRU cache to store recent QA results
qa_cache = LRUCache(maxsize=100)


def get_cached_answer(query: str) -> Optional[dict]:
    """
    Retrieve a cached result for a query, if available.

    Args:
        query (str): The user query string.

    Returns:
        Optional[dict]: Cached result if present, otherwise None.
    """
    return qa_cache.get(query)


def set_cached_answer(query: str, result: dict) -> None:
    """
    Cache the result of a query.

    Args:
        query (str): The user query string.
        result (dict): The result dictionary to cache.
    """
    qa_cache[query] = result


async def get_or_cache_qa_result(query: str, qa_chain: RetrievalQA) -> dict:
    """
    Returns a cached QA result if it exists, otherwise runs the chain and caches it.

    Args:
        query (str): The user's question.
        qa_chain (RetrievalQA): The QA chain to invoke if result isn't cached.

    Returns:
        dict: The result from cache or from chain execution.
    """
    cached = get_cached_answer(query)
    if cached:
        return cached

    # Run chain in a background thread and cache the result
    result = await run_in_threadpool(qa_chain.invoke, query)
    set_cached_answer(query, result)
    return result

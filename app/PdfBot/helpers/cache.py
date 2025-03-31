from cachetools import LRUCache
from typing import Optional

from langchain.chains import RetrievalQA
from starlette.concurrency import run_in_threadpool

qa_cache = LRUCache(maxsize=100)


def get_cached_answer(query: str) -> Optional[dict]:
    return qa_cache.get(query)


def set_cached_answer(query: str, result: dict):
    qa_cache[query] = result


async def get_or_cache_qa_result(query: str, qa_chain: RetrievalQA) -> dict:
    cached = get_cached_answer(query)
    if cached:
        return cached

    result = await run_in_threadpool(qa_chain.invoke, query)
    set_cached_answer(query, result)
    return result

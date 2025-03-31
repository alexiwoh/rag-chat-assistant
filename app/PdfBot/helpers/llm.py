from langchain_ollama import OllamaLLM
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache


def enable_llm_cache():
    """ Enable prompt-level LLM caching """
    set_llm_cache(InMemoryCache())


def get_ollama_llm():
    return OllamaLLM(
        model="mistral",
        base_url="http://host.docker.internal:11434",
        temperature=0,
        config={
            "num_ctx": 4096,
            "num_batch": 32,
            "num_thread": 6,
        }
    )

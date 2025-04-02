from langchain_ollama import OllamaLLM
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache


def enable_llm_cache() -> None:
    """
    Enable in-memory caching for LLM responses.
    This speeds up repeated prompts by storing prompt-response pairs.
    """
    set_llm_cache(InMemoryCache())


def get_ollama_llm() -> OllamaLLM:
    """
    Instantiate and return an Ollama LLM instance configured for local inference.

    Returns:
        OllamaLLM: Configured Ollama LLM for use in LangChain.
    """
    return OllamaLLM(
        model="mistral",
        base_url="http://host.docker.internal:11434",  # Ensures container can reach host Ollama instance
        temperature=0,  # Deterministic responses
        config={
            "num_ctx": 4096,      # Context window size
            "num_batch": 32,      # Batch size for inference
            "num_thread": 6,      # Number of CPU threads
        }
    )
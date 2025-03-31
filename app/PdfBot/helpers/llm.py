from langchain_ollama import OllamaLLM


def get_ollama_llm():
    return OllamaLLM(
        model="mistral",
        base_url="http://host.docker.internal:11434",
        temperature=0.1,
        config={
            "num_ctx": 4096,
            "num_batch": 32,
            "num_thread": 6,
        }
    )
from ..core.app import create_app
from ..helpers.embedding import load_vector_store
from ..helpers.llm import get_ollama_llm, enable_llm_cache
from ..helpers.chain import build_qa_chain


def initialize_components():
    app = create_app()
    enable_llm_cache()
    retriever = load_vector_store()
    llm = get_ollama_llm()
    qa_chain = build_qa_chain(llm, retriever)
    return app, qa_chain

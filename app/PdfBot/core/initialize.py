from ..core.app import create_app
from ..helpers.embedding import load_vector_store
from ..helpers.llm import get_ollama_llm
from ..helpers.chain import build_qa_chain


def initialize_components():
    """
    Initializes and wires together the core components of the RAG application.

    - Creates the FastAPI app instance
    - Loads or builds the vector store (ChromaDB) and its retriever
    - Instantiates the Ollama LLM
    - Builds the RetrievalQA chain using the retriever and LLM

    Returns:
        tuple: A tuple containing:
            - app (FastAPI): the web application instance
            - qa_chain (RetrievalQA): the retrieval-augmented question-answering chain
    """
    app = create_app()
    retriever = load_vector_store()
    llm = get_ollama_llm()
    qa_chain = build_qa_chain(llm, retriever)
    return app, qa_chain

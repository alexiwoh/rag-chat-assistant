from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores import VectorStoreRetriever

from ..constants import PROMPT_TEMPLATE_PDF_QA


def build_qa_chain(llm: BaseLanguageModel, retriever: VectorStoreRetriever) -> RetrievalQA:
    """
    Builds a RetrievalQA chain using the provided language model and retriever.

    The chain uses the 'stuff' strategy to combine retrieved documents into a single prompt,
    and applies a custom prompt template for grounded PDF-based QA.

    Args:
        llm (BaseLanguageModel): The language model to use for answering questions.
        retriever (VectorStoreRetriever): The retriever to fetch relevant documents.

    Returns:
        RetrievalQA: A configured RetrievalQA chain that returns answers and source documents.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": PROMPT_TEMPLATE_PDF_QA
        }
    )

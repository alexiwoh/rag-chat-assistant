from langchain.chains import RetrievalQA
from ..constants import PROMPT_TEMPLATE_PDF_QA


def build_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": PROMPT_TEMPLATE_PDF_QA
        }
    )

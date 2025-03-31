import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from ..constants.paths import DOCUMENTS_DEFAULT_DIRECTORY, CHROMA_DB_DEFAULT_DIRECTORY


def find_all_pdfs(root_dir: str):
    """
    Recursively finds all PDFs in a directory and loads them as LangChain documents.
    Adds source name and page metadata for attribution.
    """
    all_docs = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".pdf"):
                full_path = os.path.join(root, file)
                loader = PyMuPDFLoader(full_path)
                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = os.path.basename(doc.metadata.get("source", full_path))
                    doc.metadata["page"] = doc.metadata.get("page", None)

                print(f"📄 Loaded {len(docs)} docs from: {full_path}")
                all_docs.extend(docs)

    print(f"✅ Total documents loaded: {len(all_docs)}")
    return all_docs


def split_documents(documents, chunk_size=1024, chunk_overlap=256):
    """
    Splits documents into overlapping chunks using recursive character splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
        # splitter tries preserving paragraphs, then lines, then sentences, then words, then characters
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} text chunks.")
    return chunks


def embed_and_store_documents(split_docs, persist_directory):
    """
    Embeds document chunks using a HuggingFace model and stores them in a Chroma vector DB.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"🧠 Vector store created at: {persist_directory}")
    return vectordb


def embed_documents(
    root_dir=DOCUMENTS_DEFAULT_DIRECTORY,
    persist_directory=CHROMA_DB_DEFAULT_DIRECTORY
):
    """
    Full pipeline to load, split, embed, and persist documents into a vector store.
    """
    raw_docs = find_all_pdfs(root_dir)
    split_docs = split_documents(raw_docs)
    vectordb = embed_and_store_documents(split_docs, persist_directory)
    return vectordb


def load_vector_store():
    db = embed_documents()
    retriever = db.as_retriever(search_kwargs={"k": 4})
    return retriever

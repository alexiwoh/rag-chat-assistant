import os
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from PyPDF2 import PdfReader
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.retrievers import BaseRetriever

from ..constants import NUMBER_TOP_SOURCES, EMBEDDING_MODEL
from ..constants.paths import DOCUMENTS_DEFAULT_DIRECTORY, CHROMA_DB_DEFAULT_DIRECTORY


def find_all_pdfs(root_dir: str) -> List[Document]:
    """
    Recursively finds all PDFs in a directory and loads them as LangChain documents.
    Adds page number and extracted PDF metadata (title, author, etc.) to each document.

    Args:
        root_dir (str): Root folder to recursively search for PDF files.

    Returns:
        List[Document]: A list of documents with enriched metadata from all found PDFs.
    """
    all_docs = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".pdf"):
                full_path = os.path.join(root, file)

                # Extract metadata
                try:
                    reader = PdfReader(full_path)
                    metadata = reader.metadata or {}
                except Exception as e:
                    metadata = {}
                    print(f"⚠️ Couldn't extract PDF metadata from {file}: {e}")

                loader = PyMuPDFLoader(full_path)
                docs = loader.load()

                for doc in docs:
                    doc.metadata["source"] = os.path.basename(doc.metadata.get("source", full_path))
                    doc.metadata["page"] = doc.metadata.get("page", None)

                    # Add cleaned and stringified metadata fields
                    doc.metadata["title"] = str(metadata.get("/Title", ""))
                    doc.metadata["author"] = str(metadata.get("/Author", ""))
                    doc.metadata["subject"] = str(metadata.get("/Subject", ""))
                    doc.metadata["creation_date"] = str(metadata.get("/CreationDate", ""))
                    doc.metadata["mod_date"] = str(metadata.get("/ModDate", ""))

                print(f"📄 Loaded {len(docs)} docs from: {full_path}")
                all_docs.extend(docs)

    print(f"✅ Total documents loaded: {len(all_docs)}")
    return all_docs


def inject_metadata(doc: Document) -> str:
    """
    Appends select metadata fields into the content of the document
    to give the language model extra reasoning context during retrieval.

    Args:
        doc (Document): A LangChain Document object with metadata.

    Returns:
        str: The document's text prefixed with selected metadata.
    """
    metadata = doc.metadata
    metadata_lines = []
    if metadata.get("title"):
        metadata_lines.append(f"Title: {metadata['title']}")
    if metadata.get("author"):
        metadata_lines.append(f"Author: {metadata['author']}")
    if metadata.get("subject"):
        metadata_lines.append(f"Subject: {metadata['subject']}")
    return "\n".join(metadata_lines + [doc.page_content])


def split_documents(documents: List[Document], chunk_size: int = 1024, chunk_overlap: int = 256) -> List[Document]:
    """
    Splits documents into overlapping chunks using recursive character splitting.
    Injects metadata directly into the page content for better context.

    Args:
        documents (List[Document]): A list of documents to split.
        chunk_size (int): Size of each chunk in characters.
        chunk_overlap (int): Number of overlapping characters between chunks.

    Returns:
        List[Document]: List of chunked documents with metadata injected into their text.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
        # splitter tries preserving paragraphs, then lines, then sentences, then words, then characters
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} text chunks.")

    docs_with_metadata = [
        Document(page_content=inject_metadata(doc), metadata=doc.metadata)
        for doc in chunks
    ]

    return docs_with_metadata


def embed_and_store_documents(split_docs: List[Document], persist_directory: str) -> Chroma:
    """
    Embeds document chunks using a HuggingFace model and stores them in a Chroma vector DB.

    Args:
        split_docs (List[Document]): Chunked and metadata-injected documents to embed.
        persist_directory (str): Path to the Chroma DB persistence directory.

    Returns:
        Chroma: Initialized Chroma vector store with embedded documents.
    """
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=EMBEDDING_MODEL,
        persist_directory=persist_directory
    )
    print(f"🧠 Vector store created at: {persist_directory}")
    return vector_db


def embed_documents(
    root_dir: str = DOCUMENTS_DEFAULT_DIRECTORY,
    persist_directory: str = CHROMA_DB_DEFAULT_DIRECTORY
) -> Chroma:
    """
    Full pipeline to load, split, embed, and persist documents into a vector store.

    Args:
        root_dir (str): Root directory containing PDFs.
        persist_directory (str): Where to save the Chroma vector DB.

    Returns:
        Chroma: The resulting vector database.
    """
    raw_docs = find_all_pdfs(root_dir)
    split_docs = split_documents(raw_docs)
    vector_db = embed_and_store_documents(split_docs, persist_directory)
    return vector_db


def is_chroma_db_valid(path: str) -> bool:
    """
    Checks whether a Chroma vector DB already exists at the given path,
    including nested folders.

    Args:
        path (str): Path to check for Chroma DB files.

    Returns:
        bool: True if DB exists and contains data, else False.
    """
    print(f"🔎 Checking for database in {path}...")
    if not os.path.exists(path):
        return False

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".bin") or file.endswith(".pkl") or file.endswith(".parquet") or file.endswith(".sqlite3"):
                return True

    return False


def get_vector_store(force_rebuild: bool = False) -> Chroma:
    """
    Loads an existing Chroma vector DB if available, otherwise rebuilds it from documents.

    Args:
        force_rebuild (bool): Whether to forcefully rebuild the DB from scratch.

    Returns:
        Chroma: A Chroma vector DB, either loaded or freshly built.
    """
    if not force_rebuild and is_chroma_db_valid(CHROMA_DB_DEFAULT_DIRECTORY):
        print("🔁 Loading existing vector store...")
        vector_db = Chroma(
            persist_directory=CHROMA_DB_DEFAULT_DIRECTORY,
            embedding_function=EMBEDDING_MODEL
        )
    else:
        print("🆕 No existing vector store found. Rebuilding from documents...")
        vector_db = embed_documents()
    return vector_db


def load_vector_store() -> BaseRetriever:
    """
    Returns a retriever object using hybrid MMR-based similarity search
    with a balanced trade-off between relevance and diversity.

    Returns:
        BaseRetriever: A configured LangChain retriever for querying the vector store.
    """
    db = get_vector_store()

    # Semantic retriever: pure vector similarity
    similarity_retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": NUMBER_TOP_SOURCES}
    )

    # MMR retriever: adds diversity
    mmr_retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": NUMBER_TOP_SOURCES,
            "fetch_k": NUMBER_TOP_SOURCES * 4,
            "lambda_mult": 0.8
        }
    )

    # Sparse keyword matching retriever (BM25)
    raw_docs = find_all_pdfs(DOCUMENTS_DEFAULT_DIRECTORY)
    bm25_retriever = BM25Retriever.from_documents(raw_docs)
    bm25_retriever.k = NUMBER_TOP_SOURCES

    # Combine them using weighted ensemble
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, similarity_retriever, mmr_retriever],
        weights=[0.4, 0.4, 0.2]
    )

    return hybrid_retriever

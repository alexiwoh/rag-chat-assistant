from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

from ..constants.paths import DOCUMENTS_DEFAULT_DIRECTORY, CHROMA_DB_DEFAULT_DIRECTORY


def embed_documents(
    root_dir=DOCUMENTS_DEFAULT_DIRECTORY,
    persist_directory=CHROMA_DB_DEFAULT_DIRECTORY
):
    """
        Loads all PDF files from a directory (recursively), splits their text into chunks,
        embeds the chunks using a Hugging Face model, and stores them in a Chroma vector database.

        Args:
            root_dir (str): Root folder where documents are stored. Can include nested folders.
                            Default is 'documents'.
            persist_directory (str): Path where the Chroma vector database should be stored.
                                     Default is 'app/databases/chroma_db'.

        Returns:
            Chroma: A LangChain-compatible vector store instance, ready for similarity search.
    """
    all_docs = []

    # 1. Recursively find all PDFs
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".pdf"):
                full_path = os.path.join(root, file)
                loader = PyMuPDFLoader(full_path)
                docs = loader.load()
                print(f"Loaded {len(docs)} docs from {full_path}")
                for doc in docs:
                    print("→", doc.page_content[:200])  # Show sample content
                all_docs.extend(docs)

    print(f"📄 Loaded {len(all_docs)} documents from PDF files.")

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    split_docs = splitter.split_documents(all_docs)
    print(f"✂️ Split into {len(split_docs)} text chunks.")

    # 3. Embed & store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    vectordb.persist()
    print(f"✅ Vector store created at: {persist_directory}")
    return vectordb

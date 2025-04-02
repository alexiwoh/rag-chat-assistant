# 🧠 Rag Chat Assistant

![Run Tests](https://github.com/alexiwoh/rag-chat-assistant/actions/workflows/test.yaml/badge.svg)

A simple, containerized Retrieval-Augmented Generation (RAG) system with a web-based chat interface.  
Built with **FastAPI**, **LangChain**, and **ChromaDB** to parse, embed, index, and retrieve content from PDF documents.

---

## 🚀 Features

- 🧠 **LLM-powered RAG pipeline** built with LangChain and locally hosted via Ollama (no paid APIs)
- 📄 **PDF ingestion, metadata extraction, chunking, and embedding** using HuggingFace + ChromaDB
- 🔍 **Hybrid retrieval** for combining vector and keyword search
- ⚙️ **Prompt engineering** with few-shot reasoning, hallucination prevention, and context formatting
- 🔗 **Source attribution** with grouped page numbers per document
- 🔁 **Response caching** using `LRUCache` to speed up repeated queries
- 🌐 **Web-based UI** built with FastAPI + Jinja2 to interact with your document knowledge base in the **app/documents/** folder
- 🐳 **Fully containerized** with Docker for cross-platform deployment
- 🧪 **CI pipeline** via GitHub Actions, running `pytest` on every commit

---

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Ollama](https://ollama.com/) – local LLM server
- [Jinja2](https://jinja.palletsprojects.com/) + HTML/CSS for the chat UI
- [Docker + Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/alexiwoh/rag-chat-assistant.git
```

### 2. 💻 Requirements

Before running the app, make sure you have the following installed:

- 🐳 [Docker](https://www.docker.com/products/docker-desktop)
- 🦙 [Ollama](https://ollama.com/download) – for local LLM model inference

Both are cross-platform and free to install.

---

## 🚀 Starting the App

Once Docker and Ollama are installed and running, run the following in the Terminal:

```bash
./start-app
```

---

## 🛑 Stopping the App

Run the following in the Terminal:

```bash
./stop-app
```

---

## 🧹 Cleaning the App

Run the following in the Terminal:

```bash
./clean-app
```

To force a rebuild of the Docker image, delete the current vector database, and regenerate the vector store on the next project run, use:

```bash
./clean-app --rebuild
```

## 📥 Updating Documents

To add new knowledge to the system:

1. Drop your PDF files into the `app/documents/` folder. You can also organize them in subfolders if needed.
2. Delete the current database:
   
```bash
./clean-app --rebuild
```

3. The system will automatically reprocess all documents and rebuild the vector store the next time you launch the app:

```bash
./start-app
```

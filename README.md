# 🧠 Rag Chat Assistant

![Run Tests](https://github.com/alexanderiwoh/rag-chat-assistant/actions/workflows/test.yaml/badge.svg)

A simple, containerized Retrieval-Augmented Generation (RAG) system with a web-based chat interface.  
Built with **FastAPI**, **LangChain**, and **ChromaDB** to parse, embed, index, and retrieve content from PDF documents.

---

## 🚀 Features

- 🧠 LLM-powered agent using LangChain
- 📄 PDF ingestion, chunking, and embedding
- 🔍 Semantic search with ChromaDB
- 🌐 Web-based UI to chat with your knowledge base
- 🐳 Fully containerized with Docker
- ⚡️ One-liner startup via shell script

---

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Ollama](https://ollama.com/) – local LLM server
- [Jinja2](https://jinja.palletsprojects.com/) + HTML/CSS for the chat UI
- [Docker + Compose](https://docs.docker.com/compose/)

---

## 💻 Requirements

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

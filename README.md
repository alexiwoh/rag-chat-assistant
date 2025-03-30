# 🧠 rag-chat-assistant

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

## 🧠 Model Setup (via Ollama)

This app uses the **Mistral** model through [Ollama](https://ollama.com/), which handles model serving behind the scenes.

---

## 📦 Running the Project in the Terminal

```bash
./start-app
```

---

## 📦 Stopping the Project in the Terminal

```bash
./stop-app
```

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
- [Docker + Compose](https://docs.docker.com/compose/)
- [Jinja2](https://jinja.palletsprojects.com/) + HTML/CSS for the chat UI

---

## 🧠 Model Setup

This app uses the open-source **Mistral-7B-Instruct** model via `llama-cpp-python`.
You can get the model one of two ways:

### Option 1:

1. Visit the model page on Hugging Face:  
   👉 [TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

2. Download the file:  
   `mistral-7b-instruct-v0.1.Q4_K_M.gguf`

3. Place the file inside the `app/models/` folder so it looks like this:

<pre><code>```
app/
├── models/
│   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
```</code></pre>

### Option 2:

#### 📦 Download the Model (Run the following in the terminal)
```bash
./app/download-model.sh
```

---

## 📦 Running the Project

```bash
./start-app
```

---

## 📦 Stopping the Project

```bash
./stop-app
```

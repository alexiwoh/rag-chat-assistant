from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA

from embed_documents import embed_documents

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = embed_documents()

retriever = db.as_retriever()

llm = LlamaCpp(
    model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=4096,
    temperature=0.1,
    max_tokens=512,
    n_threads=6,  # Adjust based on your own CPU
    verbose=True
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

chat_history = []


@app.get("/", response_class=HTMLResponse)
def serve_chat(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })


@app.post("/", response_class=HTMLResponse)
def handle_chat(request: Request, query: str = Form(...)):
    result = qa_chain.invoke(query)

    answer = result["result"]
    sources = list(set(doc.metadata.get("source", "unknown") for doc in result["source_documents"]))

    # Add to chat history
    chat_history.append({
        "user": query,
        "agent": answer,
        "sources": sources
    })

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })

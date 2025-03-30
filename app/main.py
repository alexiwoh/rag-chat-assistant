from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain_community.chat_models.fake import FakeListChatModel
from langchain.chains import RetrievalQA

from embed_documents import embed_documents

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = embed_documents()

retriever = db.as_retriever()

llm = FakeListChatModel(responses=["This is a mock RAG response."])
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

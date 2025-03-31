from fastapi import Request, Form
from fastapi.responses import HTMLResponse

from PdfBot.helpers.embedding import load_vector_store
from PdfBot.helpers.llm import get_ollama_llm
from PdfBot.helpers.chain import build_qa_chain
from PdfBot.core.app import create_app
from PdfBot.helpers.chat import process_chat_request, get_chat_ui

app = create_app()
retriever = load_vector_store()
llm = get_ollama_llm()
qa_chain = build_qa_chain(llm, retriever)


@app.get("/", response_class=HTMLResponse)
def serve_chat(request: Request):
    return get_chat_ui(request)


@app.post("/", response_class=HTMLResponse)
async def handle_chat(request: Request, query: str = Form(...)):
    return await process_chat_request(query, qa_chain, request)

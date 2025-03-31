from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from PdfBot.helpers.chat import process_chat_request, get_chat_ui
from PdfBot.core import initialize_components


app, qa_chain = initialize_components()


@app.get("/", response_class=HTMLResponse)
def serve_chat(request: Request):
    return get_chat_ui(request)


@app.post("/", response_class=HTMLResponse)
async def handle_chat(request: Request, query: str = Form(...)):
    return await process_chat_request(query, qa_chain, request)

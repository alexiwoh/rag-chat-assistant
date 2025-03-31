from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from starlette.concurrency import run_in_threadpool

from PdfBot.constants import PROMPT_TEMPLATE_PDF_QA
from PdfBot.helpers import embed_documents
from PdfBot.helpers.utils import sanitize_text

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = embed_documents()
retriever = db.as_retriever()

llm = OllamaLLM(
    model="mistral",
    base_url="http://host.docker.internal:11434",
    temperature=0.1,
    config={
        "num_ctx": 4096,
        "num_batch": 32,
        "num_thread": 6,
    }
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff",  # concatenate context docs
    chain_type_kwargs={
        "prompt": PROMPT_TEMPLATE_PDF_QA
    }
)

chat_history = []


@app.get("/", response_class=HTMLResponse)
def serve_chat(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })


@app.post("/", response_class=HTMLResponse)
async def handle_chat(request: Request, query: str = Form(...)):
    try:
        if not query.strip():
            error_message = "⚠️ Query cannot be empty."
            raise ValueError(error_message)

        query_clean = sanitize_text(query)

        if len(query_clean) > 2000:
            error_message = "⚠️ Query too long. Please limit to 2000 characters."
            raise ValueError(error_message)

        result = await run_in_threadpool(qa_chain.invoke, query_clean)

        answer = result["result"]
        sources = list(set(doc.metadata.get("source", "unknown") for doc in result["source_documents"]))

        chat_history.append({
            "user": query_clean,
            "agent": answer,
            "sources": sources
        })

        return templates.TemplateResponse("chat.html", {
            "request": request,
            "chat_history": chat_history
        })

    except ValueError as ve:
        # Show validation errors in the UI
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "chat_history": chat_history,
            "error": sanitize_text(str(ve))
        })

    except Exception as e:
        # Catch-all for unexpected issues
        print(f"❌ Error during QA inference: {e}")
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "chat_history": chat_history,
            "error": f"Something went wrong: {sanitize_text(str(e))}"
        })
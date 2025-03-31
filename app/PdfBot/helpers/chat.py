from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from langchain.chains import RetrievalQA
from starlette.concurrency import run_in_threadpool

from .cache import get_cached_answer, set_cached_answer
from .utils import sanitize_text
from ..constants import MAX_INPUT_LENGTH

templates = Jinja2Templates(directory="templates")
chat_history = []


def get_chat_ui(request: Request, error: str = None):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history,
        "error": sanitize_text(error) if error else None
    })


async def safe_run_qa(query: str, qa_chain: RetrievalQA) -> dict:
    """
    Sanitizes and validates input, runs inference, and returns structured result.
    Raises ValueError for any validation or execution issues.
    """
    if not query.strip():
        raise ValueError("⚠️ Query cannot be empty.")

    query_clean = sanitize_text(query)

    if len(query_clean) > MAX_INPUT_LENGTH:
        raise ValueError(f"⚠️ Query too long. Please limit to {MAX_INPUT_LENGTH} characters.")

    cached_result = get_cached_answer(query_clean)
    if cached_result:
        result = cached_result
    else:
        result = await run_in_threadpool(qa_chain.invoke, query_clean)
        set_cached_answer(query_clean, result)

    answer = result["result"]
    sources = list(set(doc.metadata.get("source", "unknown") for doc in result["source_documents"]))

    return {
        "query": query_clean,
        "answer": answer,
        "sources": sources
    }


async def process_chat_request(query: str, qa_chain: RetrievalQA, request: Request):
    """
    High-level chat handler that catches errors and renders the UI.
    """
    try:
        result = await safe_run_qa(query, qa_chain)

        chat_history.append({
            "user": result["query"],
            "agent": result["answer"],
            "sources": result["sources"]
        })

        return get_chat_ui(request)

    except Exception as e:
        print(f"❌ Error during QA inference: {e}")
        return get_chat_ui(request, error=str(e))
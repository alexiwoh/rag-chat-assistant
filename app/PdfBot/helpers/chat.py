from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from langchain.chains import RetrievalQA

from .cache import get_or_cache_qa_result
from .utils import sanitize_text, build_source_strings, validate_and_sanitize_query

templates = Jinja2Templates(directory="templates")
chat_history = []


def get_chat_ui(request: Request, error: str = None):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history,
        "error": sanitize_text(error) if error else None
    })


async def safe_run_qa(query: str, qa_chain: RetrievalQA) -> dict:
    query_clean = validate_and_sanitize_query(query)
    result = await get_or_cache_qa_result(query_clean, qa_chain)
    answer = result["result"]

    sources = build_source_strings(result["source_documents"])
    if not sources:
        answer += "\n\n⚠️ There were no supporting sources retrieved."

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
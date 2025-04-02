from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from langchain.chains import RetrievalQA
from typing import Optional

from starlette.responses import JSONResponse

from .cache import get_or_cache_qa_result
from .utils import sanitize_text, build_source_strings, validate_and_sanitize_query
from ..constants.paths import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)
chat_history = []


def render_chat_response(request: Request, error: Optional[str] = None):
    """
    Returns either a rendered HTML page or JSON response based on `?json=true`.

    Args:
        request (Request): Incoming FastAPI request.
        error (Optional[str]): Optional error message.

    Returns:
        Union[TemplateResponse, JSONResponse]: HTML or JSON output.
    """
    error_sanitized = sanitize_text(error) if error else None
    response_payload = {
        "chat_history": chat_history,
        "error": error_sanitized
    }

    if request.query_params.get("json") == "true":
        return JSONResponse(content=response_payload)

    return templates.TemplateResponse(
        request,
        "chat.html",
        response_payload
    )


async def safe_run_qa(query: str, qa_chain: RetrievalQA) -> dict:
    """
    Executes the QA chain safely, handling validation and fallback messaging.

    Args:
        query (str): Raw user query string.
        qa_chain (RetrievalQA): The QA chain object.

    Returns:
        dict: Contains sanitized query, final answer, and source strings.
    """
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
    Handles a full chat request: runs QA, updates chat history, and renders output.
    Returns either a rendered HTML page or JSON response based on `?json=true`.

    Args:
        query (str): User query string.
        qa_chain (RetrievalQA): The chain responsible for QA inference.
        request (Request): Incoming FastAPI request object.

    Returns:
        Union[TemplateResponse, JSONResponse]: HTML or JSON output.
    """
    try:
        result = await safe_run_qa(query, qa_chain)

        chat_history.append({
            "user": result["query"],
            "agent": result["answer"],
            "sources": result["sources"]
        })

        return render_chat_response(request)

    except Exception as e:
        print(f"❌ Error during QA inference: {e}")
        return render_chat_response(request, error=str(e))

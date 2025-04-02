from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from langchain.chains import RetrievalQA
from typing import Optional

from .cache import get_or_cache_qa_result
from .utils import sanitize_text, build_source_strings, validate_and_sanitize_query
from ..constants.paths import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)
chat_history = []


def get_chat_ui(request: Request, error: Optional[str] = None):
    """
    Renders the chat UI template with chat history and optional error message.

    Args:
        request (Request): The incoming FastAPI request.
        error (Optional[str]): Optional error message to show in the UI.

    Returns:
        TemplateResponse: Rendered HTML page with chat history and errors (if any).
    """
    return templates.TemplateResponse(
        request,
        "chat.html",
        {
            "chat_history": chat_history,
            "error": sanitize_text(error) if error else None
        }
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

    Args:
        query (str): User query string.
        qa_chain (RetrievalQA): The chain responsible for QA inference.
        request (Request): Incoming FastAPI request object.

    Returns:
        TemplateResponse: The rendered chat UI with updated history or error.
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

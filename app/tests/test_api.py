from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient

from ..PdfBot.constants import MAX_INPUT_LENGTH
from ..main import app

client = TestClient(app)


def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "LangChain RAG Chat Agent" in response.text


def test_empty_query_post():
    response = client.post("/", data={"query": "   "})
    assert response.status_code == 200
    assert "Query cannot be empty" in response.text


def test_too_long_query_post():
    long_query = "a" * (MAX_INPUT_LENGTH + 1)
    response = client.post("/", data={"query": long_query})
    assert response.status_code == 200
    assert "Query too long" in response.text


@patch("PdfBot.helpers.chat.safe_run_qa", new_callable=AsyncMock)
def test_valid_query_post(mock_run):
    mock_run.return_value = {
        "query": "What is AI?",
        "answer": "AI is artificial intelligence.",
        "sources": ["example.pdf (page 1)"]
    }

    response = client.post("/", data={"query": "What is AI?"})
    assert response.status_code == 200
    assert "AI is artificial intelligence." in response.text
    assert "example.pdf" in response.text


@patch("PdfBot.helpers.chat.safe_run_qa", new_callable=AsyncMock)
def test_malicious_input_sanitization(mock_run):
    mock_run.return_value = {
        "query": "<script>alert('XSS')</script>",
        "answer": "Harmless output",
        "sources": []
    }

    response = client.post("/", data={"query": "<script>alert('XSS')</script>"})
    assert response.status_code == 200
    assert "&lt;script&gt;" in response.text
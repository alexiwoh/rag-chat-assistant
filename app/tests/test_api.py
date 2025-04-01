from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "LangChain RAG Chat Agent" in response.text

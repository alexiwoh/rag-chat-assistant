import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DOCUMENTS_DEFAULT_DIRECTORY = os.path.join(BASE_DIR, "documents")
CHROMA_DB_DEFAULT_DIRECTORY = os.path.join(BASE_DIR, "databases", "chroma_db")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")

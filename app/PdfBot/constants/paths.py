import os

# === Base Directory ===
# Resolve base directory two levels up from this file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# print(f"[paths.py] BASE_DIR: {BASE_DIR}")  # DEBUG

# === Documents Directory ===
# Directory where documents (PDFs) are expected to be found
DOCUMENTS_DEFAULT_DIRECTORY = os.path.join(BASE_DIR, "documents")
# print(f"[paths.py] DOCUMENTS_DEFAULT_DIRECTORY: {DOCUMENTS_DEFAULT_DIRECTORY}")  # DEBUG

# === Chroma Vector DB Directory ===
# Directory where the Chroma vector DB will be stored
CHROMA_DB_DEFAULT_DIRECTORY = os.path.join(BASE_DIR, "databases", "chroma_db")
# print(f"[paths.py] CHROMA_DB_DEFAULT_DIRECTORY: {CHROMA_DB_DEFAULT_DIRECTORY}")  # DEBUG

# === Templates Directory ===
# Directory for HTML templates (used in FastAPI Jinja2Templates)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")
# print(f"[paths.py] TEMPLATES_DIR: {os.path.abspath(TEMPLATES_DIR)}")  # DEBUG

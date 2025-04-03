from langchain_huggingface import HuggingFaceEmbeddings

NUMBER_OF_SOURCES_DISPLAY = 3
NUMBER_TOP_SOURCES = 6

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)

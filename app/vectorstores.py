from langchain_chroma import Chroma
from .config import CHROMA_DOCS_DIR,CHROMA_MEMORY_DIR

from .embeddings import get_embeddings

def get_document_db():
    return Chroma(
        collection_name="all_data",
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DOCS_DIR,
    )

def get_memory_db():
    return Chroma(
        collection_name='long-term-memory',
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_MEMORY_DIR,
    )
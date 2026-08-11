# ============================================================
# 0. CONFIG
# ============================================================

LM_STUDIO_BASE_URL="http://127.0.0.1:1234/v1"
LM_STUDIO_MODEL="google/gemma-4-e2b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DOCS_DIR="./chroma_db"
CHROMA_MEMORY_DIR="./memory_db"
RETRIEVER_K = 3
MEMORY_K = 3
SHOW_DEBUG = True
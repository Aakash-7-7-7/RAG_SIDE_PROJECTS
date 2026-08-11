from .config import RETRIEVER_K
from .vectorstores import get_document_db

db=get_document_db()

retriever=db.as_retriever(
    search_kwargs={"k":RETRIEVER_K}
)

def retrieve_documents(query:str):
    return retriever.invoke(query)

def build_context(documents):
    unique_chunks = []
    seen = set()

    for doc in documents:
        content = doc.page_content.strip()

        if content in seen:
            continue

        # Skip chunks that are near-fully contained in an already-included
        # chunk (handles the 150-char overlap between adjacent chunks from
        # ingestion, which otherwise gets echoed twice by the model).
        if any(content in existing or existing in content for existing in unique_chunks):
            continue

        seen.add(content)
        unique_chunks.append(content)

    return "\n\n".join(unique_chunks)
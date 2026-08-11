from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHROMA_DOCS_DIR
from .embeddings import get_embeddings
from .vectorstores import get_document_db


DATA_DIR = Path("data")


def load_pdfs():
    documents = []

    for pdf_file in DATA_DIR.glob("*.pdf"):

        print(f"Loading: {pdf_file.name}")

        loader = PyMuPDFLoader(str(pdf_file))

        pdf_documents = loader.load()

        documents.extend(pdf_documents)

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    return chunks


def ingest():

    print("\n--- Loading PDFs ---")

    documents = load_pdfs()

    print(f"Loaded {len(documents)} pages.")

    print("\n--- Splitting documents ---")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\n--- Creating Chroma database ---")

    db = get_document_db()

    db.add_documents(chunks)

    print("\n--- Ingestion complete ---")
    print(f"Stored documents in: {CHROMA_DOCS_DIR}")


if __name__ == "__main__":
    ingest()
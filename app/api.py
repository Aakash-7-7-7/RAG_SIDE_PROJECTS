from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .pipeline import RAGMemoryPipeline


app = FastAPI(
    title="RAG Side Quest",
    description="Local RAG assistant with long-term memory",
    version="1.0.0",
)

# Allow the frontend (served separately, e.g. from a different port or
# opened as a local file) to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


chat = RAGMemoryPipeline()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def home():
    return {
        "message": "RAG Side Quest API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    result = chat.ask(request.question)

    # Only the question and final answer are exposed to clients.
    # Internal details (rewritten question, running summary, extracted
    # memories) stay server-side - use SHOW_DEBUG / the CLI if you need
    # to inspect them.
    return {
        "question": result["question"],
        "answer": result["answer"],
    }
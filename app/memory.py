from .config import MEMORY_K
from .models import get_llm
from .prompts import memory_prompt
from .vectorstores import get_memory_db
from .utils import clean

memory_db=get_memory_db()
llm=get_llm()
memory_chain=memory_prompt | llm

def get_memories(query:str)->list[str]:
    docs=memory_db.similarity_search(
        query,
        k=MEMORY_K
    )
    return[
        doc.page_content
        for doc in docs
    ]

def extract_memories(
        question:str,
        answer:str,
)->str:

    response=memory_chain.invoke({
        "question":question,
        "answer":answer,
    })
    return clean(response.content)

def save_memories(raw_text:str):
    if raw_text.strip().upper()=="NONE":
        return
    memories=[
        memory.strip()
        for memory in raw_text.split("\n")
        if memory.strip()
    ]
    if memories:
        memory_db.add_texts(memories)
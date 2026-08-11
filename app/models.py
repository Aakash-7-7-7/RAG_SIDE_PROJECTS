from .config import *
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model=LM_STUDIO_MODEL,
        base_url=LM_STUDIO_BASE_URL,
        api_key="lm-studio",
        temperature=0
    )
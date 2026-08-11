from .models import get_llm
from .prompts import summary_prompt
from .utils import clean

llm=get_llm()

summary_chain=summary_prompt | llm

def update_summary(
        summary:str,
        question:str,
        answer:str,
)->str:
    response=summary_chain.invoke({
        "summary":summary,
        "question":question,
        "answer":answer,
    })
    return clean(response.content)
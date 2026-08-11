from .models import get_llm
from .prompts import rewrite_prompt
from .utils import clean

llm=get_llm()

rewrite_chain=rewrite_prompt | llm

def rewrite_question(
        question:str,
        summary:str,
        memories:str,
)-> str:
    response=rewrite_chain.invoke({
        "summary":summary,
        "memories":memories,
        "question":question,

    })

    return clean(response.content)
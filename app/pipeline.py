from concurrent.futures import ThreadPoolExecutor

from .models import get_llm
from .prompts import answer_prompt
from .utils import clean

from .memory import get_memories,extract_memories,save_memories

from .summary import update_summary
from .question_retriever import rewrite_question

from .retriever import retrieve_documents,build_context

llm=get_llm()

answer_chain=answer_prompt | llm 

class RAGMemoryPipeline:
    def __init__(self):
        self.conversation_summary=""
        self.pool=ThreadPoolExecutor(
            max_workers=2
        )

    def ask(self,question:str):
        memories=get_memories(question)
        memory_text="\n".join(memories)

        if self.conversation_summary or memory_text:
            standalone_question=rewrite_question(
                question,
                self.conversation_summary,
                memory_text,
            )

        else:
            standalone_question=question


        documents=retrieve_documents(
            standalone_question
        )
        context=build_context(documents)

        response=answer_chain.invoke({
            "question":standalone_question,
            "context":context,
        })
        answer=clean(response.content)
        summary_future = self.pool.submit(
            update_summary,
            self.conversation_summary,
            question,
            answer,
        )

        memory_future=self.pool.submit(
            extract_memories,question,answer,
        )

        self.conversation_summary= summary_future.result()
        

        extracted_memories= memory_future.result()
        

        save_memories(extracted_memories)

        return{
            "question": question,
            "standalone_question": standalone_question,
            "answer": answer,
            "summary": self.conversation_summary,
            "memories": extracted_memories,
        }
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# 5. PROMPTS / CHAINS
# ============================================================

rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You rewrite the user's latest question into a standalone question.\n\n"
     "Use the conversation summary and relevant long-term memories to "
     "understand references such as: it, that, they, this, the previous one.\n\n"
     "Do NOT answer the question. Return ONLY the rewritten question, with no "
     "explanation, preamble, or reasoning."),
    ("human",
     "Conversation Summary:\n{summary}\n\n"
     "Relevant Long-Term Memories:\n{memories}\n\n"
     "Current Question:\n{question}"),
])


answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful RAG assistant.\n\n"
     "Answer the user's question using the provided context, in your own "
     "words. If the answer cannot be found in the context, say that you "
     "don't know. Do not invent information.\n\n"
     "The context may contain overlapping or repeated passages - do not "
     "copy it verbatim, and never state the same fact or sentence more than "
     "once in your answer. Write each point a single time.\n\n"
     "You may privately work through the context first if that helps you. "
     "But your response MUST end with a line that says exactly:\n"
     "FINAL ANSWER:\n"
     "followed by ONLY the direct answer to the user's question - written "
     "in full sentences, with no meta-commentary, no restating the question, "
     "and no notes about your own process. Everything the user will actually "
     "see is what comes after 'FINAL ANSWER:', so that section must stand "
     "completely on its own.\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])


memory_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Identify information from this interaction that is worth remembering "
     "for future conversations.\n\n"
     "Store only useful persistent information such as: user preferences, "
     "project information, technical choices, goals, important requirements.\n\n"
     "Do NOT store: greetings, temporary questions, normal explanations, "
     "information useful only for this conversation.\n\n"
     "If there is nothing worth remembering, return: NONE\n"
     "Otherwise return each memory on a separate line. No extra commentary."),
    ("human", "User:\n{question}\n\nAssistant:\n{answer}"),
])


summary_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You maintain a running conversation summary.\n\n"
     "Merge the existing summary with the new interaction into a single, "
     "updated summary written as your own concise prose/bullets. Keep only "
     "what's needed to understand future questions: current topic, "
     "important technical details, decisions, unresolved questions.\n\n"
     "Output ONLY the updated summary text itself - a few sentences or "
     "short bullet points. Do NOT include labels like 'Summary:', "
     "'New Interaction:', 'User:', or 'Assistant:'. Do NOT copy the question "
     "or answer verbatim - integrate their meaning into the summary. Do NOT "
     "repeat any point that is already covered. No reasoning, no preamble."),
    ("human",
     "Existing Summary:\n{summary}\n\n"
     "New Interaction:\nUser:\n{question}\n\nAssistant:\n{answer}"),
])
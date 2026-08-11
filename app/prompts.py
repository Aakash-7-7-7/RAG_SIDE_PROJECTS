from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# 5. PROMPTS / CHAINS
# ============================================================

rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You rewrite the user's latest question into a standalone question.\n\n"
     "First, check whether the Current Question actually depends on the "
     "Conversation Summary or Memories to make sense - i.e. does it contain "
     "a reference like: it, that, they, this, the previous one, or is it "
     "clearly a follow-up to what was just discussed?\n\n"
     "- If YES: use the summary/memories ONLY to resolve that reference, "
     "producing a standalone version of the SAME question. Do not add "
     "scope, sub-topics, or angles the user didn't ask about.\n"
     "- If NO - i.e. the question is already self-contained, or it is about "
     "a completely different topic than the summary/memories - IGNORE the "
     "summary and memories entirely and return the Current Question "
     "unchanged (only fixing obvious grammar/casing if needed). Do NOT "
     "blend it with the previous topic just because a summary exists.\n\n"
     "When in doubt, prefer returning the question unchanged over rewriting "
     "it - only rewrite when there is a clear reference that needs "
     "resolving.\n\n"
     "Do NOT answer the question. Return ONLY the rewritten (or unchanged) "
     "question, with no explanation, preamble, or reasoning."),
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
     "don't know. If Something else is aksed say only say i dont know no other topic .Do not invent information, details, or claims that are "
     "not present in the context - stay close to what the context actually "
     "says rather than elaborating beyond it.\n\n"
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
     "Use ONLY what was actually said in the User/Assistant exchange below. "
     "Do NOT add any fact, example, or detail that was not explicitly "
     "present in it, even if it seems plausible - these memories are stored "
     "permanently and reused in future conversations, so anything invented "
     "here will corrupt future answers.\n\n"
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
     "CRITICAL: Use ONLY information that appears in the Existing Summary "
     "or the New Interaction shown to you below. Do NOT add any fact, "
     "example, entity, name, statistic, or claim that is not explicitly "
     "present in those two sources - even if it seems relevant or true. "
     "If you are unsure whether something was actually said, leave it out. "
     "This summary will be reused as context for future answers, so "
     "introducing anything not actually discussed will corrupt those "
     "answers.\n\n"
     "Output ONLY the updated summary text itself - a few sentences or "
     "short bullet points. Do NOT include any heading or label such as "
     "'Summary:', 'Updated Summary:', 'New Interaction:', 'User:', or "
     "'Assistant:' anywhere in your response - start directly with the "
     "content. Do NOT copy the question or answer verbatim - integrate "
     "their meaning into the summary. Do NOT repeat any point that is "
     "already covered. No reasoning, no preamble."),
    ("human",
     "Existing Summary:\n{summary}\n\n"
     "New Interaction:\nUser:\n{question}\n\nAssistant:\n{answer}"),
])
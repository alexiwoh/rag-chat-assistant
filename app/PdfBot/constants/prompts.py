from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE_PDF_QA = PromptTemplate.from_template("""
You are an intelligent assistant tasked with answering user questions based on provided context only.

Use the context below to answer the question. 
If the context is insufficient or unrelated, say "I don't know" — do not make up an answer.

Context:
{context}

Question: {question}
Answer:
""")

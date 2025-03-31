from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE_PDF_QA = PromptTemplate.from_template("""
You are a helpful assistant that answers questions based only on the provided context.

Always follow these rules:
- Only answer using the information in the context.
- If the answer is not in the context, say "I don't know based on the given information."
- Explain your reasoning step by step if the question is complex.

Context:
{context}

---

Here are some examples to guide you:

Q: What are the key risks of AI mentioned?
A: Let's think step by step. The context mentions several risks including bias, misuse, and lack of transparency. So, the key risks are bias, misuse, and lack of transparency.

Q: Who published the paper?
A: The context does not include the name of the publisher. I don't know based on the given information.

---

Now, answer the following question:

Q: {question}
A:
""")

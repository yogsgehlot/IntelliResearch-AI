class PromptBuilder:

    @staticmethod
    def build(
        context: str,
        question: str,
    ) -> str:

        return f"""
You are an Enterprise AI Research Assistant.

Answer ONLY using the supplied context.

If the answer is not available, reply:

"I couldn't find the answer in the uploaded documents."

--------------------

Context

{context}

--------------------

Question

{question}

--------------------

Answer:
"""
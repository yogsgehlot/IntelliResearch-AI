from app.ai.llm.ollama_client import OllamaClient


class QueryRewriter:

    def __init__(self):
        self.llm = OllamaClient()

    def rewrite(
        self,
        question: str,
        history: str,
    ):
        if history:
            prompt = f"""
Given the following conversation history and the latest user question, rewrite it into a standalone question.
Only incorporate context from the history if the latest question explicitly refers to it (using pronouns or references like "it", "they", "him", "her", "that", "first paper", etc.).
If the latest question is a new query or a standalone topic, DO NOT add or invent details from the history.
Correct any obvious spelling mistakes, typos, or name variations (e.g., "Kennath" -> "Kenneth") to ensure accurate retrieval.
Return ONLY the standalone rewritten question. Do not include any intro, explanation, or conversational text.

Conversation History:
{history}

Latest Question:
{question}

Standalone Question:
"""
        else:
            prompt = f"""
Given the user's question, correct any obvious spelling mistakes, typos, or name variations (e.g., "Kennath" -> "Kenneth") and return it as a clean standalone search query.
Return ONLY the corrected question. Do not include any intro, explanation, or conversational text.

User Question:
{question}

Standalone Question:
"""

        return self.llm.generate(prompt).strip()
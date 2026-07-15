from app.ai.llm.ollama_client import OllamaClient

client = OllamaClient()

def general_tool(state):
    answer = client.generate(state["question"])
    state["answer"] = answer
    return state
from app.ai.rag.rag_service import RAGService


def rag_tool(state):

    rag = RAGService()

    result = rag.ask(
        project_id=state["project_id"],
        session_id=state["session_id"],
        question=state["question"],
    )

    state["answer"] = result["answer"]
    state["sources"] = result["sources"]

    return state
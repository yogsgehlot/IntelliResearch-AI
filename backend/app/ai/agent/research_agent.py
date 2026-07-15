def router(state):

    question = state["question"].lower()
    keywords = [
        "document",
        "paper",
        "pdf",
        "uploaded",
        "research",
    ]

    if any( word in question for word in keywords):
        return "rag"

    return "general"
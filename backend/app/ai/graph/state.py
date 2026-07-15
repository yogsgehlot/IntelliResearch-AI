from typing import TypedDict


class GraphState(TypedDict):

    project_id: str

    session_id: str

    question: str

    context: str

    history: str

    answer: str

    sources: list

    route: str
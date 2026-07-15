from app.core.startup import initialize_ai
from app.ai.graph.graph import graph

initialize_ai()

# state = {
#     "project_id": "YOUR_PROJECT_ID",
#     "session_id": "session-1",
#     "question": "Summarize the uploaded paper.",
#     "context": "",
#     "history": "",
#     "answer": "",
#     "sources": [],
#     "route": "",
# }

state["question"] = "Who proposed it?"

result = graph.invoke(state)

print(result["answer"])
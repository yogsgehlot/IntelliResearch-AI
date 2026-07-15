from langgraph.graph import StateGraph
from langgraph.graph import END
from app.ai.graph.state import GraphState
from app.ai.agent.research_agent import router
from app.ai.tools.general_tool import general_tool
from app.ai.tools.rag_tool import rag_tool

workflow = StateGraph(GraphState)
workflow.add_node("rag",rag_tool,)
workflow.add_node("general",general_tool,)

workflow.set_conditional_entry_point(
    router,
    {
        "rag": "rag",
        "general": "general",
    },
)

workflow.add_edge("rag",END,)
workflow.add_edge("general",END,)

graph = workflow.compile()
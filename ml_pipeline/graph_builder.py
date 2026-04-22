from langgraph.graph import StateGraph, END
from ml_pipeline.state import GraphState
from ml_pipeline.graph_nodes import load_csv_data, classifier_agent, reasoning_agent, format_output

def create_sentiment_graph():
    """Create the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("load_csv", load_csv_data)
    workflow.add_node("classify", classifier_agent)
    workflow.add_node("reason", reasoning_agent)
    workflow.add_node("format", format_output)

    workflow.set_entry_point("load_csv")
    workflow.add_edge("load_csv", "classify")
    workflow.add_edge("classify", "reason")
    workflow.add_edge("reason", "format")
    workflow.add_edge("format", END)

    return workflow.compile()

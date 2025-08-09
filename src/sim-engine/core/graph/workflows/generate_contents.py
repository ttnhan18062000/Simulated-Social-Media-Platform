from langgraph.graph import StateGraph, END
from ..models.generate_content_models import GraphState
from ..nodes.generate_content_nodes import (
    generate_persona,
    generate_topic,
    generate_draft,
    quality_check,
    rewrite_content,
)


def build_generate_content_workflow():
    """
    Builds a LangGraph workflow that runs:
    persona → topic → draft → quality check → rewrite
    """
    workflow = StateGraph(GraphState)

    # Register nodes
    workflow.add_node("generate_persona", generate_persona)
    workflow.add_node("generate_topic", generate_topic)
    workflow.add_node("generate_draft", generate_draft)
    workflow.add_node("quality_check", quality_check)
    workflow.add_node("rewrite_content", rewrite_content)

    # Edges in sequence
    workflow.add_edge("generate_persona", "generate_topic")
    workflow.add_edge("generate_topic", "generate_draft")
    workflow.add_edge("generate_draft", "quality_check")
    workflow.add_edge("quality_check", "rewrite_content")
    workflow.add_edge("rewrite_content", END)

    # Set entry point
    workflow.set_entry_point("generate_persona")

    return workflow.compile()


def run_generate_content_workflow(initial_state: GraphState):
    """
    Runs the compiled workflow with the given initial state.
    Returns the final GraphState with all intermediate results.
    """
    workflow = build_generate_content_workflow()
    return workflow.invoke(initial_state)

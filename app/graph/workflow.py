from langgraph.graph import (
    StateGraph,
    END,
)

from app.models.state import (
    GraphState,
)

from app.graph.nodes.extract_state import (
    extract_state_node,
)

from app.graph.nodes.detect_intent import (
    detect_intent_node,
)

from app.graph.nodes.clarify import (
    clarify_node,
)

from app.graph.nodes.respond import (
    respond_node,
)

from app.graph.nodes.retrieve import (
    retrieve_node,
)

from app.graph.nodes.planning import (
    planning_node,
)

from app.graph.nodes.explain import (
    explain_node,
)


graph = StateGraph(GraphState)


graph.add_node(
    "extract_state",
    extract_state_node,
)

graph.add_node(
    "detect_intent",
    detect_intent_node,
)

graph.add_node(
    "clarify",
    clarify_node,
)

graph.add_node(
    "respond",
    respond_node,
)


graph.set_entry_point(
    "extract_state"
)

graph.add_edge(
    "extract_state",
    "planning",
)

graph.add_edge(
    "planning",
    "detect_intent",
)

def route_intent(state):

    intent = state["intent"]

    if intent == "CLARIFY":

        return "clarify"
    if intent == "EXPLAIN":

        return "explain"

    return "retrieve"


graph.add_conditional_edges(

    "detect_intent",

    route_intent,

    {

        "clarify": "clarify",

        "retrieve": "retrieve",
        "explain": "explain",
    },
)


graph.add_edge(
    "clarify",
    END,
)

graph.add_edge(
    "respond",
    END,
)

graph.add_edge(
    "retrieve",
    "respond",
)

graph.add_edge(
    "explain",
    END,
)

graph.add_node(
    "retrieve",
    retrieve_node,
)

graph.add_node(
    "planning",
    planning_node,
)

graph.add_node(
    "explain",
    explain_node,
)

workflow = graph.compile()


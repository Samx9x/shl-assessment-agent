from app.retrieval.reasoning.ambiguity_detector import (
    detect_ambiguity,
)


def detect_intent_node(state):

    context = state[
        "hiring_context"
    ]

    llm_plan = state[
        "llm_plan"
    ]

    last_message = state[
        "messages"
    ][-1]["content"].lower()

    # EXPLANATION INTENT

    if (

        "why" in last_message

        or

        "reason" in last_message

        or

        "suggested" in last_message

        or

        "recommended" in last_message
    ):

        state["intent"] = (
            "EXPLAIN"
        )

        return state

    if (
        "compare" in last_message
    ):

        state["intent"] = (
            "COMPARE"
        )

        return state

    if (

        "add" in last_message

        or "remove" in last_message

        or "instead" in last_message
    ):

        state["intent"] = (
            "REFINE"
        )

        return state

    ambiguity, reason = (
        detect_ambiguity(
            context
        )
    )

    if (

        llm_plan.get(
            "clarification_needed"
        )

        and

        not context.role
    ):

        ambiguity = True

        reason = "llm_clarification"

    state[
        "ambiguity_detected"
    ] = ambiguity

    state[
        "ambiguity_reason"
    ] = reason

    print("\nINTENT DEBUG:\n")

    print(
        "ROLE:",
        context.role
    )

    print(
        "AMBIGUITY:",
        ambiguity
    )

    print(
        "LLM CLARIFICATION:",
        llm_plan.get(
            "clarification_needed"
        )
    )

    print("\n") 

    if ambiguity:

        state["intent"] = (
            "CLARIFY"
        )

        return state

    state["intent"] = (
        "RECOMMEND"
    )

    return state
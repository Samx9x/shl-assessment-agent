def clarify_node(state):

    llm_plan = state[
        "llm_plan"
    ]

    reason = state.get(
        "ambiguity_reason",
        "",
    )

    question = llm_plan.get(
        "clarification_question"
    )

    if reason == "missing_role":

        question = (
            "What role are you hiring for?"
        )

    elif (
        reason
        ==
        "developer_specialization"
    ):

        question = (
            "What type of developer "
            "are you hiring?"
        )

    elif (
        reason
        ==
        "missing_seniority"
    ):

        question = (
            "What seniority level "
            "are you hiring for?"
        )

    elif (
        reason
        ==
        "manager_seniority"
    ):

        question = (
            "What management level "
            "are you hiring for?"
        )

    if not question:

        question = (
            "Could you clarify "
            "your hiring needs?"
        )

    state["final_response"] = {

        "reply": question,

        "recommendations": [],

        "end_of_conversation": False,
    }

    return state
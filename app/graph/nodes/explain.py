def explain_node(state):

    last_message = state[
        "messages"
    ][-1]["content"].lower()

    response = (
        "This assessment was "
        "recommended because it "
        "matches the role requirements."
    )

    if "automata" in last_message:

        response = (
            "Automata Front End was "
            "recommended because it "
            "evaluates practical frontend "
            "development skills through "
            "simulations."
        )

    elif (
        "opq" in last_message
        or
        "opq32r" in last_message
    ):

        response = (
            "OPQ32r was recommended "
            "because it evaluates workplace "
            "behavior, personality traits, "
            "and team fit."
        )

    elif (
        "verify" in last_message
        or
        "g+" in last_message
    ):

        response = (
            "Verify - G+ was recommended "
            "because it measures cognitive "
            "ability and problem-solving skills."
        )

    elif "reactjs" in last_message:

        response = (
            "ReactJS (New) was recommended "
            "because it assesses React "
            "frontend development skills."
        )

    elif "javascript" in last_message:

        response = (
            "JavaScript (New) was recommended "
            "because it evaluates core "
            "JavaScript programming skills."
        )

    state["final_response"] = {

        "reply": response,

        "recommendations": [],

        "end_of_conversation": False,
    }

    return state
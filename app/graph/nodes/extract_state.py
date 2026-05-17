from app.models.state import (
    HiringContext,
)

from app.utils.helpers import (
    extract_role,
    extract_skills,
    detect_seniority,
)

from app.retrieval.reasoning.dimension_detector import (
    detect_dimensions,
)


def extract_state_node(state):

    context = HiringContext()

    messages = state["messages"]

    full_text = " ".join(

        [

            msg["content"]

            for msg in messages

            if msg["role"] == "user"
        ]
    )

    latest_user_message = ""

    for msg in reversed(messages):

        if msg["role"] == "user":

            latest_user_message = (
                msg["content"]
            )

            break

    pivot_phrases = [

        "actually",

        "instead",

        "change",

        "rather",

        "not frontend",

        "customer support",
    ]

    use_latest_only = any(

        phrase in
        latest_user_message.lower()

        for phrase in pivot_phrases
    )

    if use_latest_only:

        extraction_text = (
            latest_user_message
        )

    else:

        extraction_text = (
            full_text
        )

    context.role = (
        extract_role(extraction_text)
    )

    context.skills = (
        extract_skills(full_text)
    )

    context.seniority = (
        detect_seniority(full_text)
    )

    behavioral_keywords = [

        "stakeholder",
        "communication",
        "teamwork",
        "leadership",
        "collaboration",
    ]

    for keyword in (
        behavioral_keywords
    ):

        if keyword in (
            full_text.lower()
        ):

            context.behavioral_traits.append(
                keyword
            )

    context.assessment_dimensions = (
        detect_dimensions(context)
    )

    assistant_messages = [

        msg["content"].lower()

        for msg in messages

        if msg["role"] == "assistant"
    ]

    recommendation_signals = [

        "recommended shl assessments",

        "recommendations",

        "here are",

        "i recommend",
    ]

    context.has_recommended = any(

        any(
            signal in msg

            for signal in recommendation_signals
        )

        for msg in assistant_messages
    )

    print("\nEXTRACTED CONTEXT:\n")
    print(context)
    print("\n")
    state["hiring_context"] = context

    return state
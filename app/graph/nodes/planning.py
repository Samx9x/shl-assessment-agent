from app.llm.planner import (
    generate_plan,
)
from app.config.runtime import (
    REPLAY_MODE,
)


def planning_node(state):

    messages = state[
        "messages"
    ]

    conversation = "\n".join(

        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )
    if REPLAY_MODE:

        state["llm_plan"] = {

            "role_family":
            context.role,

            "technical_focus":
            context.skills,

            "behavioral_focus":
            context.behavioral_traits,

            "recommended_dimensions":
            context.assessment_dimensions,

            "clarification_needed":
            False,

            "clarification_question":
            "",
        }

        return state
    
    plan = generate_plan(
        conversation
    )
    context = state[
        "hiring_context"
    ]

    if context.role:

        plan["role_family"] = (
            context.role
        )
    state["llm_plan"] = plan

    return state
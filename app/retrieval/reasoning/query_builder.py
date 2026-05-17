def build_query(context):

    parts = []

    if context.role:

        parts.append(
            context.role
        )

    if context.skills:

        parts.extend(
            context.skills
        )

    if (
        context.behavioral_traits
    ):

        parts.extend(
            context.behavioral_traits
        )

    if context.seniority:

        parts.append(
            context.seniority
        )

    return " ".join(parts)
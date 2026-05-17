def build_dimension_queries(
    context,
    llm_plan,
):

    role = context.role or ""

    technical_focus = (
        llm_plan.get(
            "technical_focus",
            []
        )
    )

    behavioral_focus = (
        llm_plan.get(
            "behavioral_focus",
            []
        )
    )

    dimensions = (
        llm_plan.get(
            "recommended_dimensions",
            []
        )
    )

    queries = []

    if (
        "Technical Skills"
        in str(dimensions)

        or "technical"
        in str(dimensions).lower()
    ):

        role_lower = ""

        if role:

            role_lower = role.lower()

        extra_keywords = ""

        if "react" in role_lower:

            extra_keywords += (
                " react reactjs "
                "frontend javascript "
                "ui components "
            )

        if "frontend" in role_lower:

            extra_keywords += (
                " frontend javascript "
                "html css ui "
            )

        if "java" in role_lower:

            extra_keywords += (
                " java spring backend "
                "api microservices "
            )

        if "backend" in role_lower:

            extra_keywords += (
                " backend api "
                "microservices server "
            )

        tech_query = (
            f"{role} "
            + " ".join(
                technical_focus
            )
            + " "
            + extra_keywords
        )

        queries.append(

            {
                "dimension":
                "technical",

                "query":
                tech_query,
            }
        )

    if (
        "Cognitive"
        in str(dimensions)

        or "cognitive"
        in str(dimensions).lower()
    ):

        queries.append(

            {
                "dimension":
                "cognitive",

                "query":
                (
                    "Verify aptitude "
                    "reasoning general ability"
                ),
            }
        )

    if (
        "Personality"
        in str(dimensions)

        or "personality"
        in str(dimensions).lower()
    ):

        behavior_query = (
            "personality communication "
            "stakeholder teamwork "
            + " ".join(
                behavioral_focus
            )
        )

        queries.append(

            {
                "dimension":
                "behavioral",

                "query":
                behavior_query,
            }
        )

    if (
        "Simulation"
        in str(dimensions)

        or "simulation"
        in str(dimensions).lower()
    ):

        queries.append(

            {
                "dimension":
                "simulation",

                "query":
                (
                    "simulation coding "
                    "automata real world"
                ),
            }
        )

    return queries
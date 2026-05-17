def detect_ambiguity(context):

    if not context.role:

        return (
            True,
            "missing_role",
        )

    role = ""

    if context.role:

        role = context.role.lower()

    # GENERIC DEVELOPER

    if (
        "developer" in role
        and "backend" not in role
        and "frontend" not in role
    ):

        return (
            True,
            "developer_specialization",
        )

    # MANAGER SENIORITY

    if (
        "manager" in role
        and not context.seniority
    ):

        return (
            True,
            "manager_seniority",
        )

    # BROAD ENGINEERING ROLES

    broad_roles = [

        "backend developer",

        "frontend developer",

        "software engineer",

        "engineer",
    ]

    if (

        role in broad_roles

        and

        not context.seniority
    ):

        return (
            True,
            "missing_seniority",
        )

    return (
        False,
        "",
    )
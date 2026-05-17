from app.core.taxonomy import (
    ROLE_SPECIALIZATIONS,
)


def compute_role_score(

    role,
    document_text,
):

    if not role:

        return 0

    role_lower = ""

    if role:

        role_lower = role.lower()

    document_text = (
        document_text.lower()
    )

    boost = 0

    keywords = (
        ROLE_SPECIALIZATIONS.get(
            role_lower,
            [],
        )
    )

    for keyword in keywords:

        if keyword in document_text:

            boost += 2

    # STRONG ROLE-SPECIFIC BOOSTS

    if (
        "react" in role_lower
        and
        "react" in document_text
    ):

        boost += 8

    if (
        "frontend" in role_lower
        and
        "frontend" in document_text
    ):

        boost += 5

    if (
        "javascript" in role_lower
        and
        "javascript" in document_text
    ):

        boost += 5

    if (
        "java" in role_lower
        and
        "java" in document_text
    ):

        boost += 8

    if (
        "backend" in role_lower
        and
        "backend" in document_text
    ):

        boost += 5

    if (
        "customer support"
        in role_lower

        and

        (
            "contact center"
            in document_text

            or

            "customer service"
            in document_text

            or

            "phone simulation"
            in document_text
        )
    ):

        boost += 8

    return boost
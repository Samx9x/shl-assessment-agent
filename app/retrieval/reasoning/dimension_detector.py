from app.core.taxonomy import (
    ROLE_DIMENSION_MAP,
)


def detect_dimensions(context):

    role = (
        context.role.lower()
        if context.role
        else ""
    )

    dimensions = (
        context.assessment_dimensions
    )

    for pattern, mapping in (
        ROLE_DIMENSION_MAP.items()
    ):

        if pattern in role:

            for key, value in (
                mapping.items()
            ):

                dimensions[key] = value

    behavioral_keywords = [

        "stakeholder",
        "communication",
        "teamwork",
        "leadership",
        "collaboration",
    ]

    for trait in (
        context.behavioral_traits
    ):

        for keyword in behavioral_keywords:

            if keyword in trait.lower():

                dimensions[
                    "personality"
                ] = True

                dimensions[
                    "communication"
                ] = True

    return dimensions
from app.core.recommendation_policy import (
    ROLE_BASED_PREFERENCES,
)


def compute_policy_score(

    role,
    metadata,
):

    if not role:

        return 0

    role_preferences = (
        ROLE_BASED_PREFERENCES.get(
            role,
            {},
        )
    )

    category = metadata[
        "test_type"
    ]

    preferred_keywords = (
        role_preferences.get(
            category,
            [],
        )
    )

    name = metadata[
        "name"
    ].lower()

    boost = 0

    for keyword in preferred_keywords:

        if keyword.lower() in name:

            boost += 8

    return boost
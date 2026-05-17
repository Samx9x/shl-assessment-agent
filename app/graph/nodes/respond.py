from app.llm.recommendation_selector import (
    select_recommendations,
)

from app.validation.catalog_validator import (
    validate_recommendations,
)


def respond_node(state):

    context = state[
        "hiring_context"
    ]

    candidates = state[
        "candidate_results"
    ]

    clean_role = (
        context.role
    )

    clean_role = clean_role.replace(
        " react frontend",
        ""
    )

    clean_role = clean_role.replace(
        " frontend",
        ""
    )

    clean_role = clean_role.strip()

    selection = (
        select_recommendations(

            query=(
                f"{clean_role} hiring"
            ),

            candidates=candidates[:15],
        )
    )
    print(
        "\nGEMINI SELECTION:\n",
        selection,
        "\n",
    )

    selected_names = set(

        selection.get(
            "selected_names",
            []
        )
    )

    final_recommendations = []

    for item in candidates:

        metadata = item[
            "metadata"
        ]

        if (
            metadata["name"]
            not in selected_names
        ):

            continue

        final_recommendations.append(

            {

                "name": metadata[
                    "name"
                ],

                "url": metadata[
                    "url"
                ],

                "test_type": metadata[
                    "test_type"
                ],
            }
        )

    if not final_recommendations:

        for item in candidates[:5]:

            metadata = item[
                "metadata"
            ]

            final_recommendations.append(

                {

                    "name": metadata[
                        "name"
                    ],

                    "url": metadata[
                        "url"
                    ],

                    "test_type": metadata[
                        "test_type"
                    ],
                }
            )

    validated, errors = (
        validate_recommendations(
            final_recommendations
        )
    )

    print("\nVALIDATION REPORT:\n")

    if errors:

        print(
            "VALIDATION ERRORS:\n",
            errors,
        )

    else:

        print(
            "All recommendations validated "
            "against catalog."
        )

    print("\n")   

    print(
        "\nFINAL RECOMMENDATIONS:\n"
    )

    for rec in validated:

        print(
            rec["name"],
            " --> ",
            rec["test_type"]
        )

    print("\n")

    state["final_response"] = {

        "reply": selection.get(
            "reply",
            (
                f"Here are recommended "
                f"SHL assessments for "
                f"{context.role}."
            )
        ),

        "recommendations": (
            validated[:5]
        ),

        "end_of_conversation": False,
    }

    return state
from app.core.taxonomy import (
    DEFAULT_BATTERIES,
)


def build_battery_plan(context):

    dimensions = (
        context.assessment_dimensions
    )

    planned_categories = []

    for dimension, enabled in (
        dimensions.items()
    ):

        if not enabled:
            continue

        categories = (
            DEFAULT_BATTERIES.get(
                dimension,
                [],
            )
        )

        for category in categories:

            if (
                category
                not in planned_categories
            ):

                planned_categories.append(
                    category
                )

    return planned_categories
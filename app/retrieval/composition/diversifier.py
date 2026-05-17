def diversify_results(

    results,
    battery_plan,
    limit=5,
):

    grouped = {}

    for category in battery_plan:

        grouped[category] = []

    for item in results:

        category = item[
            "metadata"
        ]["test_type"]

        if category in grouped:

            grouped[
                category
            ].append(item)

    final = []

    for category in battery_plan:

        if grouped[category]:

            final.append(
                grouped[category][0]
            )

    remaining = []

    for category_items in (
        grouped.values()
    ):

        remaining.extend(
            category_items[1:]
        )

    remaining = sorted(

        remaining,

        key=lambda x: x[
            "final_score"
        ],

        reverse=True,
    )

    for item in remaining:

        if len(final) >= limit:

            break

        final.append(item)

    return final[:limit]
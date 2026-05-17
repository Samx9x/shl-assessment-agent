from app.catalog.loader import (
    catalog_data,
)


catalog_lookup = {}

for item in catalog_data:

    catalog_lookup[
        item["name"]
    ] = item


def validate_recommendations(
    recommendations,
):

    validated = []

    errors = []

    for rec in recommendations:

        name = rec.get(
            "name"
        )

        if (
            name
            not in catalog_lookup
        ):

            errors.append(

                {
                    "name": name,
                    "error": (
                        "Assessment not found "
                        "in catalog"
                    ),
                }
            )

            continue

        catalog_item = (
            catalog_lookup[name]
        )

        expected_url = (
            catalog_item.get(
                "link",
                ""
            )
        )

        expected_type = (
            catalog_item.get(
                "keys",
                ["Unknown"]
            )[0]
        )

        if (
            rec.get("url")
            != expected_url
        ):

            errors.append(

                {
                    "name": name,
                    "error": (
                        "URL mismatch"
                    ),

                    "expected": (
                        expected_url
                    ),

                    "received": (
                        rec.get("url")
                    ),
                }
            )

        if (
            rec.get("test_type")
            != expected_type
        ):

            errors.append(

                {
                    "name": name,

                    "error": (
                        "Test type mismatch"
                    ),

                    "expected": (
                        expected_type
                    ),

                    "received": (
                        rec.get(
                            "test_type"
                        )
                    ),
                }
            )

        validated.append(

            {

                "name": name,

                "url": expected_url,

                "test_type": (
                    expected_type
                ),
            }
        )

    return validated, errors
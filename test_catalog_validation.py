from app.validation.catalog_validator import (
    validate_recommendations,
)


fake_response = [

    {
        "name":
        "Java Frameworks (New)",

        "url":
        "https://wrong-url.com",

        "test_type":
        "Wrong Type",
    },

    {
        "name":
        "Fake Assessment",

        "url":
        "https://fake.com",

        "test_type":
        "Fake",
    },
]


validated, errors = (
    validate_recommendations(
        fake_response
    )
)

print("\nVALIDATED:\n")
print(validated)

print("\nERRORS:\n")
print(errors)
import re


def normalize_text(text: str):

    return text.lower().strip()


def extract_skills(text: str):

    SKILL_KEYWORDS = [

        "java",
        "python",
        "react",
        "javascript",
        "spring",
        "sql",
        "aws",
        "cloud",
        "api",
        "backend",
        "frontend",
        "salesforce",
        "pega",
        "support",
    ]

    text = normalize_text(text)

    found = []

    for skill in SKILL_KEYWORDS:

        if skill in text:

            found.append(skill)

    return found


def detect_seniority(text: str):

    text = normalize_text(text)

    mapping = {

        "intern": "Entry-Level",

        "junior": "Entry-Level",

        "graduate": "Graduate",

        "entry": "Entry-Level",

        "mid": "Mid-Professional",

        "senior": "Manager",

        "lead": "Manager",

        "manager": "Manager",

        "director": "Director",

        "executive": "Executive",
    }

    for key, value in mapping.items():

        if key in text:

            return value

    return None


def extract_role(text: str):

    text = normalize_text(text)

    role_patterns = [

        r"(frontend react developer)",

        r"(react developer)",

        r"(frontend developer)",

        r"(backend java developer)",

        r"(java backend developer)",

        r"(backend developer)",

        r"(java developer)",

        r"(python developer)",

        r"(software engineer)",

        r"(data analyst)",

        r"(sales manager)",

        r"(customer support executive)",

        r"(customer support)",

        r"(graduate software engineer)",

        r"(graduate trainee)",

        r"(developer)",

        r"(engineer)",
    ]

    for pattern in role_patterns:

        match = re.search(
            pattern,
            text,
        )

        if match:

            role = (
                match.group(1)
                .title()
            )

            role = role.replace(
                "Java Backend Developer",
                "Backend Developer"
            )

            role = role.replace(
                "Backend Java Developer",
                "Backend Developer"
            )

            role = role.replace(
                "Frontend React Developer",
                "Frontend Developer"
            )

            role = role.replace(
                "React Developer",
                "Frontend Developer"
            )


            role = role.replace(
                "Graduate Software Engineer",
                "Software Engineer"
            )

            return role

    return None
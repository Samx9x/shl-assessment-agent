import json
import re

from app.llm.gemini_client import (
    model,
)


SYSTEM_PROMPT = """
You are an SHL assessment recommendation expert.

You are given:
1. Hiring requirements
2. A list of candidate SHL assessments

Your task:

- Keep reply under 2 short sentences
- Do not explain every recommendation
- Keep tone concise and recruiter-like
- Select the BEST assessments
- Ensure balanced coverage
- Prefer recruiter-quality batteries
- Prefer technical + cognitive + personality balance when appropriate

Reply Rules:

- Keep replies under 10 words when possible
- Do not explain assessment coverage unless asked
- Match concise recruiter tone
- Example:
  "Here are recommended SHL assessments for a Frontend Developer role."

IMPORTANT:
- ONLY choose assessments from provided candidates
- NEVER invent assessments
- NEVER invent URLs
- Return STRICT JSON only

Schema:

{
  "reply": "",
  "selected_names": []
}

Reply should be concise like:
"Here are recommended SHL assessments for a backend developer role."
"""


def extract_json(text):

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace(
        "```",
        ""
    )

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL,
    )

    if not match:

        return None

    return match.group(0)


def select_recommendations(

    query,
    candidates,
):

    formatted = []

    for idx, item in enumerate(
        candidates
    ):

        metadata = item[
            "metadata"
        ]

        formatted.append(

            f"""
Candidate {idx + 1}

Name:
{metadata['name']}

Type:
{metadata['test_type']}

URL:
{metadata['url']}
"""
        )

    prompt = f"""
Hiring Query:
{query}

Candidate Assessments:
{''.join(formatted)}
"""

    response = model.generate_content(

        SYSTEM_PROMPT
        + "\n\n"
        + prompt
    )

    raw = response.text

    try:

        parsed = json.loads(
            extract_json(raw)
        )

        return parsed

    except Exception:

        return {

            "reply": (
                "Here are recommended "
                "SHL assessments."
            ),

            "selected_names": [],
        }
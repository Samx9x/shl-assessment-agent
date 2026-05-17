import json
import re

from app.llm.gemini_client import (
    model,
)


SYSTEM_PROMPT = """
You are an SHL hiring assessment strategist.

Analyze the hiring conversation.

Return STRICT JSON only.

Schema:

{
  "role_family": "",
  "technical_focus": [],
  "behavioral_focus": [],
  "recommended_dimensions": [],
  "clarification_needed": false,
  "clarification_question": ""
}

Rules:

Role Guidance:

- Backend developers:
  technical + cognitive + personality

- Frontend developers:
  frontend technical + simulation + cognitive + personality

- Customer support:
  simulation + personality + communication

- Leadership:
  personality + competencies

- Graduate hiring:
  aptitude + technical + personality

- Ask clarification questions ONLY if:
  ambiguity materially affects recommendations.



- NEVER return markdown.

- NEVER explain your answer.

Role Mapping Rules:

- Frontend React developers are frontend engineers
- React developers are frontend engineers
- Java backend developers are backend engineers
- Customer support executives are customer service roles
- Graduate software engineers are software engineering roles

Never classify React/frontend roles as backend developers.

Return ONLY valid JSON.
"""


def extract_json(text):

    text = text.strip()

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


def generate_plan(conversation_text):

    prompt = f"""
Conversation:
{conversation_text}
"""

    response = model.generate_content(
        SYSTEM_PROMPT
        + "\n\n"
        + prompt
    )

    raw_text = response.text

    try:

        json_text = extract_json(
            raw_text
        )

        if not json_text:

            raise ValueError(
                "No JSON found"
            )

        parsed = json.loads(
            json_text
        )

        print(
            "\nLLM PLAN:\n",
            parsed,
            "\n",
        )

        return parsed

    except Exception as e:

        print(
            "\nPLANNER ERROR:\n",
            e,
        )

        print(
            "\nRAW LLM RESPONSE:\n",
            raw_text,
            "\n",
        )

        return {

            "role_family": "",

            "technical_focus": [],

            "behavioral_focus": [],

            "recommended_dimensions": [],

            "clarification_needed": False,

            "clarification_question": "",
        }
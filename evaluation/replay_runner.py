import sys

from pathlib import Path

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)

sys.path.append(
    str(ROOT_DIR)
)

import google.generativeai as genai
from app.llm.key_manager import (
    get_trace_key,
)
import json
import re
import requests
from pathlib import Path
from app.config import runtime

runtime.REPLAY_MODE = True

API_URL = (
    "http://127.0.0.1:8000/chat"
)

TRACE_DIR = Path(
    "evaluation/public_traces"
)

GENERATED_DIR = Path(
    "evaluation/generated_traces"
)

STRUCTURED_DIR = Path(
    "evaluation/structured"
)

GENERATED_DIR.mkdir(
    exist_ok=True
)

STRUCTURED_DIR.mkdir(
    exist_ok=True
)


def parse_trace_markdown(
    text,
):

    pattern = re.compile(

        r"\*\*User\*\*\s*> (.*?)\n\n\*\*Agent\*\*",

        re.DOTALL,
    )

    matches = pattern.findall(
        text
    )

    messages = []

    for msg in matches:

        messages.append(

            {
                "role": "user",

                "content":
                msg.strip(),
            }
        )

    return messages


def generate_markdown_trace(
    trace_name,
    turns,
):

    md = [
        "# Conversation\n"
    ]

    for idx, turn in enumerate(
        turns,
        start=1,
    ):

        md.append(
            f"\n## Turn {idx}\n"
        )

        md.append(
            "\n**User**\n"
        )

        md.append(
            f"\n> {turn['user']}\n"
        )

        md.append(
            "\n**Agent**\n"
        )

        md.append(
            f"\n{turn['assistant_reply']}\n"
        )

        recs = turn.get(
            "recommendations",
            []
        )

        if recs:

            md.append(
                "\n| # | Name | Test Type | URL |\n"
            )

            md.append(
                "|---|---|---|---|\n"
            )

            for i, rec in enumerate(
                recs,
                start=1,
            ):

                md.append(

                    f"| {i} | "

                    f"{rec['name']} | "

                    f"{rec['test_type']} | "

                    f"{rec['url']} |\n"
                )

    return "".join(md)


def replay_trace(
    trace_file,
):
    trace_name = (
        trace_file.stem
    )

    api_key = (
        get_trace_key(
            trace_name
        )
    )

    if api_key:

        genai.configure(
            api_key=api_key
        )

        print(
            f"\nUSING API KEY "
            f"FOR {trace_name}\n"
        )

    print(
        f"\nRUNNING "
        f"{trace_file.name}\n"
    )

    text = trace_file.read_text(
        encoding="utf-8"
    )

    user_messages = (
        parse_trace_markdown(
            text
        )
    )

    conversation = []

    generated_turns = []

    for msg in user_messages:

        conversation.append(
            msg
        )

        payload = {

            "messages":
            conversation
        }

        try:

            response = (
                requests.post(

                    API_URL,

                    json=payload,

                    timeout=60,
                )
            )

            data = (
                response.json()
            )

        except Exception as e:

            print(
                "\nREQUEST FAILED:\n",
                e,
            )

            print(
                "\nRAW RESPONSE:\n",
                response.text
                if 'response' in locals()
                else "NO RESPONSE"
            )

            data = {

                "reply":
                f"ERROR: {e}",

                "recommendations":
                [],
            }

        assistant_msg = {

            "role":
            "assistant",

            "content":
            data.get(
                "reply",
                ""
            ),
        }

        conversation.append(
            assistant_msg
        )

        generated_turns.append(

            {

                "user":
                msg["content"],

                "assistant_reply":
                data.get(
                    "reply",
                    ""
                ),

                "recommendations":
                data.get(
                    "recommendations",
                    []
                ),
            }
        )

    # SAVE JSON

    json_path = (

        STRUCTURED_DIR

        /

        f"{trace_file.stem}.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(

            generated_turns,

            f,

            indent=2,
        )

    # SAVE MARKDOWN

    markdown = (
        generate_markdown_trace(

            trace_file.stem,

            generated_turns,
        )
    )

    md_path = (

        GENERATED_DIR

        /

        f"{trace_file.stem}_generated.md"
    )

    md_path.write_text(

        markdown,

        encoding="utf-8",
    )

    print(
        f"SAVED: {md_path}"
    )


def main():

    traces = list(

        TRACE_DIR.glob(
            "*.md"
        )
    )

    print(
        f"\nFOUND "
        f"{len(traces)} "
        f" TRACE FILES\n"
    )

    for trace in traces[:1]:

        replay_trace(
            trace
        )


if __name__ == "__main__":

    main()
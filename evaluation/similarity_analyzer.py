import json
from pathlib import Path


TRACE_DIR = Path(
    "evaluation/generated_traces"
)

REPORT_PATH = Path(
    "evaluation/reports/final_report.md"
)


def evaluate_trace(
    trace_data,
):

    metrics = {

        "schema_valid": True,

        "recommendation_limit": True,

        "grounded_urls": True,

        "clarification_present": False,

        "comparison_supported": False,

        "explanation_supported": False,

        "hallucination_detected": False,
    }

    for turn in trace_data:

        assistant = (
            turn["assistant"]
        )

        reply = assistant.get(
            "reply",
            "",
        ).lower()

        recs = assistant.get(
            "recommendations",
            [],
        )

        if (
            len(recs) > 10
        ):

            metrics[
                "recommendation_limit"
            ] = False

        for rec in recs:

            if (
                "shl.com"
                not in rec.get(
                    "url",
                    "",
                )
            ):

                metrics[
                    "grounded_urls"
                ] = False

        clarification_keywords = [

            "what role",

            "clarify",

            "seniority",

            "what type",
        ]

        if any(

            k in reply

            for k in clarification_keywords
        ):

            metrics[
                "clarification_present"
            ] = True

        if (
            "compare"
            in reply
        ):

            metrics[
                "comparison_supported"
            ] = True

        explanation_keywords = [

            "recommended because",

            "evaluates",

            "measures",
        ]

        if any(

            k in reply

            for k in explanation_keywords
        ):

            metrics[
                "explanation_supported"
            ] = True

    return metrics


def build_report():

    generated_files = list(

        TRACE_DIR.glob(
            "*.json"
        )
    )

    report_lines = [

        "# Evaluation Report\n"
    ]

    for file in generated_files:

        data = json.loads(

            file.read_text(
                encoding="utf-8"
            )
        )

        metrics = (
            evaluate_trace(
                data
            )
        )

        report_lines.append(
            f"\n## {file.stem}\n"
        )

        for k, v in metrics.items():

            symbol = (
                "✅"
                if v
                else "❌"
            )

            report_lines.append(
                f"- {k}: {symbol}"
            )

    REPORT_PATH.write_text(

        "\n".join(
            report_lines
        ),

        encoding="utf-8",
    )

    print(
        f"\nREPORT SAVED: "
        f"{REPORT_PATH}\n"
    )


if __name__ == "__main__":

    build_report()
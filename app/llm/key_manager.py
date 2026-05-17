from app.config.gemini_keys import (
    GEMINI_API_KEYS,
)


def get_trace_key(
    trace_name,
):

    trace_name = (
        trace_name.upper()
    )

    return GEMINI_API_KEYS.get(
        trace_name
    )
import re

THINK_TAG_RE = re.compile(
    r"<(think|thinking|reasoning)>.*?</\1>",
    flags=re.DOTALL | re.IGNORECASE,
)

FINAL_ANSWER_RE = re.compile(
    r"FINAL ANSWER:\s*(.*)",
    flags=re.DOTALL | re.IGNORECASE,
)

# Fallback patterns: if the model forgot the FINAL ANSWER: marker, drop any
# leading lines that look like scratch-work/reasoning rather than answer text.
REASONING_LINE_RE = re.compile(
    r"^\s*(\d+\.\s*)?\*{0,2}(analyz|scan|step|first,? i|i need to|i will|"
    r"i should|let me|the user is asking|draft the answer|synthesiz)",
    flags=re.IGNORECASE,
)


# Strips a leading heading line like "**Updated Summary:**" or "Summary:"
# that some models add despite being told not to.
LEADING_HEADING_RE = re.compile(
    r"^\s*\*{0,2}(updated\s+)?summary:?\*{0,2}\s*\n+",
    flags=re.IGNORECASE,
)


def clean(text: str) -> str:

    if not text:
        return ""

    text = THINK_TAG_RE.sub("", text).strip()
    text = LEADING_HEADING_RE.sub("", text).strip()

    # If the model followed instructions, everything after FINAL ANSWER:
    # is the real answer - use only that.
    match = FINAL_ANSWER_RE.search(text)
    if match:
        return match.group(1).strip()

    # Fallback: no marker found. Strip any leading lines that look like
    # reasoning/scratch-work rather than the actual answer.
    lines = text.split("\n")
    while lines and REASONING_LINE_RE.match(lines[0]):
        lines.pop(0)

    return "\n".join(lines).strip()
import json
import re


def extract_json(text: str):
    """
    Extract valid JSON from LLM output.
    Handles:
    - text before JSON
    - text after JSON
    - both arrays and objects
    """

    if not text or text.strip() == "":
        raise ValueError("Model returned empty output")

    # Match either object {...} or array [...]
    pattern = r'(\{[\s\S]*\}|\[[\s\S]*\])'
    match = re.search(pattern, text)

    if not match:
        raise ValueError("No JSON detected in model output:\n" + text)

    json_str = match.group(1).strip()
    return json.loads(json_str)

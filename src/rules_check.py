import os
from dotenv import load_dotenv
from groq import Groq

from .json_utils import extract_json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RULES = [
    "Act must define key terms",
    "Act must specify eligibility criteria",
    "Act must specify responsibilities of the administering authority",
    "Act must include enforcement or penalties",
    "Act must include payment calculation or entitlement structure",
    "Act must include record-keeping or reporting requirements",
]


def run_rule_checks(full_text: str, sections: dict) -> list:
    """
    For each rule, returns:
    {
      "rule": str,
      "status": "pass" | "fail" | "partial",
      "evidence": str,
      "confidence": int
    }
    """

    import json as _json

    prompt = f"""
You are auditing the Universal Credit Act 2025 against six compliance rules.

Rules:
{_json.dumps(RULES, indent=2)}

You are given:
1. The full Act text.
2. Pre-extracted section summaries (definitions, obligations, responsibilities, etc.).

For each rule, decide:
- "status": "pass", "fail", or "partial"
- "evidence": specific sections/paragraphs or quotes supporting your decision
- "confidence": integer 0–100

Return ONLY valid JSON as an array of objects in this format:

[
  {{
    "rule": "Act must define key terms",
    "status": "pass",
    "evidence": "Section 2 defines 'universal credit', 'standard allowance', ...",
    "confidence": 92
  }},
  ...
]

Do NOT add any explanation before or after the JSON.

Full Act text:
{full_text[:15000]}

Section summaries:
{_json.dumps(sections, indent=2)}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    raw = response.choices[0].message.content
    # Uncomment for debugging:
    # print("RAW RULE CHECKS OUTPUT:\n", raw)
    checks = extract_json(raw)

    if not isinstance(checks, list):
        raise ValueError("Rule checks JSON is not a list")

    return checks

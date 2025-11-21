import os
from dotenv import load_dotenv
from groq import Groq

from .json_utils import extract_json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_key_sections(text: str) -> dict:
    """
    Extracts key legislative sections as concise summaries:
    - definitions
    - obligations
    - responsibilities
    - eligibility
    - payments
    - penalties
    - record_keeping
    """

    prompt = f"""
You are a legal analysis assistant.

From the Universal Credit Act 2025, extract concise summaries
for the following categories:

- "definitions": Definitions of key terms and concepts.
- "obligations": Duties imposed on claimants or other parties.
- "responsibilities": Responsibilities of the administering authority.
- "eligibility": Conditions to qualify for Universal Credit.
- "payments": Payments and entitlements, including how amounts are determined.
- "penalties": Offences, sanctions, or enforcement mechanisms.
- "record_keeping": Record-keeping and reporting duties.

Return ONLY valid JSON with EXACTLY these keys:

{{
  "definitions": "...",
  "obligations": "...",
  "responsibilities": "...",
  "eligibility": "...",
  "payments": "...",
  "penalties": "...",
  "record_keeping": "..."
}}

Reference sections or paragraphs where possible.
Do not add any explanation before or after the JSON.

Act text:
{text[:15000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    # Uncomment for debugging:
    # print("RAW SECTIONS OUTPUT:\n", raw)
    sections = extract_json(raw)

    # Basic sanity check for keys
    expected_keys = {
        "definitions",
        "obligations",
        "responsibilities",
        "eligibility",
        "payments",
        "penalties",
        "record_keeping",
    }
    if not isinstance(sections, dict) or not expected_keys.issubset(sections.keys()):
        raise ValueError("Sections JSON missing expected keys")

    return sections

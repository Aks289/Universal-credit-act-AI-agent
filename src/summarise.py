import os
import json
from dotenv import load_dotenv
from groq import Groq
from typing import List
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json(text: str):
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model output:\n" + text)
    return json.loads(match.group(1))

def summarise_act(text: str) -> List[str]:

    prompt = f"""
You are a legal analysis assistant.

Summarize the Universal Credit Act 2025 in 5–10 bullet points covering:
- Purpose
- Key definitions
- Eligibility
- Obligations
- Enforcement

Return ONLY a JSON array of bullet points.
Act text:
{text[:20000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    return extract_json(raw)

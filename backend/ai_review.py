# in this ai_review we will write logic

import requests
import json
from config import LLM_API_URL, LLM_MODEL
import re 


def safe_parse_json(text: str):
    """
    Extract and safely parse JSON from LLM output.
    Falls back gracefully if parsing fails.
    """
    try:
        # Try direct parse first
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return {"issues": []}

    json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # LAST RESORT: return empty but valid structure
        return {
            "issues": [
                {
                    "issue_type": "ParsingError",
                    "severity": "Low",
                    "line_number": None,
                    "explanation": "AI response could not be parsed reliably.",
                    "improved_code": None
                }
            ]
        }

def review_code(code: str, language: str):
    prompt = f"""
You are a senior software engineer and code reviewer.

Your task is to review the following {language} code and identify:
1. Bugs
2. Security issues
3. Performance problems
4. Code quality or best-practice improvements

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT add explanations outside JSON
- Do NOT wrap JSON in markdown
- If no issues are found, return an empty list

JSON FORMAT:
{{
  "issues": [
    {{
      "issue_type": "Bug | Security | Performance | Quality",
      "severity": "Low | Medium | High",
      "line_number": 1,
      "explanation": "Clear and concise explanation",
      "improved_code": "Improved or safer version of the code (if applicable)"
    }}
  ]
}}

CODE TO REVIEW:
{code}
"""

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(LLM_API_URL, json=payload, timeout=120)
    response.raise_for_status()

    # Ollama / LLM response
    raw_output = response.json()["message"]["content"]

    # Extract JSON safely (LLMs sometimes add text)
    json_start = raw_output.find("{")
    json_end = raw_output.rfind("}") + 1

    if json_start == -1 or json_end == -1:
        raise ValueError("Invalid JSON returned by LLM")

    parsed_json = safe_parse_json(raw_output)

    return parsed_json

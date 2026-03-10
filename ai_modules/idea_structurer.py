import json
from utils.gemini_client import get_gemini_client


def structure_startup_idea(raw_idea: str) -> dict:
    client = get_gemini_client()

    prompt = f"""
You are a startup analyst AI.

Convert the following startup idea into structured JSON.

Return ONLY valid JSON with these fields:
- startup_name
- target_users
- problem
- solution
- business_model
- market
- key_assumptions

Rules:
- key_assumptions must be a list of strings.
- Return only JSON.
- Do not use markdown fences.

Startup idea:
{raw_idea}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "startup_name": "",
            "target_users": "",
            "problem": raw_idea,
            "solution": "",
            "business_model": "",
            "market": "",
            "key_assumptions": [
                "Model response was not valid JSON."
            ],
        }
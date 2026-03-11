import json
from utils.gemini_client import get_gemini_client


def simulate_future_scenarios(structured_idea: dict, scoring: dict) -> dict:
    client = get_gemini_client()

    prompt = f"""
You are a startup strategy analyst.

Based on the startup idea and scoring below, simulate 3 possible future scenarios.

Return ONLY valid JSON in this format:

{{
  "best_case": "string",
  "realistic_case": "string",
  "worst_case": "string",
  "key_triggers": ["string", "string", "string"]
}}

Rules:
- best_case should describe what happens if execution goes very well.
- realistic_case should describe the most likely outcome.
- worst_case should describe failure or major struggle.
- key_triggers must be a list of the main factors that determine which scenario happens.
- Return only JSON, no markdown.

Startup idea:
{structured_idea}

Startup scoring:
{scoring}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception as e:
        print("Scenario parsing error:", e)
        print("Scenario raw output:", text)

        return {
            "best_case": "Could not generate best-case scenario.",
            "realistic_case": "Could not generate realistic scenario.",
            "worst_case": "Could not generate worst-case scenario.",
            "key_triggers": ["Model response was not valid JSON."]
        }
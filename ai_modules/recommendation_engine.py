import json
from utils.gemini_client import get_gemini_client


def generate_recommendations(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict,
    risks: dict
) -> dict:
    client = get_gemini_client()

    prompt = f"""
You are a startup advisor.

Based on the startup idea, scoring, future scenarios, and risk analysis below, recommend the next best actions for the founder.

Return ONLY valid JSON in this format:

{{
  "next_steps": ["string", "string", "string", "string", "string"],
  "mvp_suggestion": "string",
  "validation_focus": "string"
}}

Rules:
- next_steps should be 5 concrete actions.
- mvp_suggestion should describe the simplest MVP worth building.
- validation_focus should explain what should be tested first.
- Return only JSON, no markdown.

Startup idea:
{structured_idea}

Startup scoring:
{scoring}

Future scenarios:
{scenarios}

Risk analysis:
{risks}
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
        print("Recommendation parsing error:", e)
        print("Recommendation raw output:", text)

        return {
            "next_steps": ["Could not generate recommendations."],
            "mvp_suggestion": "Recommendation generation failed.",
            "validation_focus": "Unknown."
        }
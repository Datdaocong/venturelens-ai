import json
from utils.gemini_client import get_gemini_client


def analyze_risks(structured_idea: dict, scoring: dict, scenarios: dict) -> dict:
    client = get_gemini_client()

    prompt = f"""
You are a startup risk analyst.

Based on the startup idea, scoring, and future scenarios below, identify the main risks and dangerous assumptions.

Return ONLY valid JSON in this format:

{{
  "top_risks": ["string", "string", "string"],
  "dangerous_assumptions": ["string", "string", "string"],
  "risk_summary": "string"
}}

Rules:
- top_risks should be the 3 biggest business/product risks.
- dangerous_assumptions should be the 3 assumptions most likely to break the startup.
- risk_summary should be short and practical.
- Return only JSON, no markdown.

Startup idea:
{structured_idea}

Startup scoring:
{scoring}

Future scenarios:
{scenarios}
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
        print("Risk parsing error:", e)
        print("Risk raw output:", text)

        return {
            "top_risks": ["Could not analyze risks."],
            "dangerous_assumptions": ["Model response was not valid JSON."],
            "risk_summary": "Risk analysis failed."
        }
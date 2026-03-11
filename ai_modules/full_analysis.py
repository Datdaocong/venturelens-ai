import json
from utils.gemini_client import get_gemini_client


def generate_full_analysis(startup_idea: str) -> dict:
    client = get_gemini_client()

    prompt = f"""
You are an elite startup strategy analyst.

Analyze the startup idea below and return ONLY valid JSON in this exact format:

{{
  "structured_idea": {{
    "startup_name": "string",
    "target_users": "string",
    "problem": "string",
    "solution": "string",
    "business_model": "string",
    "market": "string",
    "key_assumptions": ["string", "string", "string"]
  }},
  "scoring": {{
    "overall_score": number,
    "scores": {{
      "problem_severity": number,
      "market_size": number,
      "competition": number,
      "differentiation": number,
      "monetization": number,
      "feasibility": number,
      "distribution": number,
      "speed_to_mvp": number
    }},
    "summary": "string"
  }},
  "scenarios": {{
    "best_case": "string",
    "realistic_case": "string",
    "worst_case": "string",
    "key_triggers": ["string", "string", "string"]
  }},
  "risks": {{
    "top_risks": ["string", "string", "string"],
    "dangerous_assumptions": ["string", "string", "string"],
    "risk_summary": "string"
  }},
  "recommendations": {{
    "next_steps": ["string", "string", "string", "string", "string"],
    "mvp_suggestion": "string",
    "validation_focus": "string"
  }}
}}

Rules:
- Return only JSON
- No markdown
- All scores must be from 1 to 10
- Be practical, realistic, and strategically sharp

Startup idea:
{startup_idea}
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
        print("Full analysis parsing error:", e)
        print("Raw output:", text)
        return {
            "structured_idea": {},
            "scoring": {
                "overall_score": 0,
                "scores": {},
                "summary": "Analysis failed."
            },
            "scenarios": {},
            "risks": {},
            "recommendations": {}
        }
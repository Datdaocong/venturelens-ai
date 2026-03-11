import json
from utils.gemini_client import get_gemini_client


def score_startup(structured_idea: dict):

    client = get_gemini_client()

    prompt = f"""
You are a venture capital analyst.

Evaluate the following startup idea and score it.

Return ONLY valid JSON.

Format:

{{
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
 "summary": "short explanation"
}}

Score each criterion from 1 to 10.

Startup idea:
{structured_idea}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Gemini đôi khi trả ```json block → phải remove
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)

    except Exception as e:
        print("Parsing error:", e)
        print("Model output:", text)

        return {
            "overall_score": 0,
            "scores": {},
            "summary": "Model response was not valid JSON"
        }
import json
from utils.gemini_client import get_gemini_client


def score_startup(structured_idea: dict) -> dict:

    client = get_gemini_client()

    prompt = f"""
You are a startup investor evaluating a startup idea.

Analyze the startup idea below and score it.

Return ONLY JSON.

Criteria (score from 1 to 10):

problem_severity
market_size
competition
differentiation
monetization
feasibility
distribution
speed_to_mvp

Also include:
overall_score
summary

Startup idea:

{structured_idea}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    try:
        return json.loads(text)

    except:
        return {
            "overall_score": 0,
            "scores": {},
            "summary": "Model response not valid JSON"
        }
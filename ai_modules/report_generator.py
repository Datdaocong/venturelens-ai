from utils.gemini_client import get_gemini_client


def generate_report(structured, scoring, scenarios, risks, recommendations):
    client = get_gemini_client()

    prompt = f"""
You are a high-level startup strategy advisor.

Write a founder briefing that feels like a serious consultant report delivered to the founder of an early-stage startup.

Writing style requirements:
- Professional, vivid, sharp, and insightful
- Sound like a strategic advisor, not a chatbot
- Do not sound robotic
- Do not mention JSON, structured data, or "provided information"
- Be concise but meaningful
- Highlight both opportunity and danger
- Make the founder feel they are receiving serious strategic advice
- Open with 2-3 sentences framing the startup as a real business opportunity under evaluation

Structure the report exactly with these headings:

# Founder Briefing
# Startup Overview
# Strategic Evaluation
# Future Scenarios
# Key Risks
# Strategic Recommendations

Extra formatting requirements:
- In Strategic Evaluation, mention the overall score naturally
- In Future Scenarios, use these subheadings:
  ## Best-Case Scenario
  ## Realistic Scenario
  ## Worst-Case Scenario
- In Key Risks, use bullet points
- In Strategic Recommendations, use numbered action steps
- Avoid repeating the same sentence structure too often
- Make the report read smoothly, like a briefing memo

Startup idea:
{structured}

Scoring:
{scoring}

Scenarios:
{scenarios}

Risks:
{risks}

Recommendations:
{recommendations}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
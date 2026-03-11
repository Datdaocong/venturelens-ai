from utils.gemini_client import get_gemini_client


def generate_report(structured, scoring, scenarios, risks, recommendations):
    client = get_gemini_client()

    prompt = f"""
You are a high-level startup strategy advisor.

Your job is to write a compelling founder briefing, as if you are presenting a strategic assessment to the founder of an early-stage startup.

Writing style requirements:
- Professional, vivid, sharp, and insightful
- Make it feel like a real startup strategy report
- Speak directly about the startup with confidence and clarity
- Do not sound robotic
- Do not mention JSON or say "based on the provided data"
- Be concise but rich in insight
- Highlight both opportunity and danger
- Make the founder feel like they are receiving serious strategic advice
- Open with 2-3 sentences that frame the startup like a serious business opportunity under evaluation.

Structure the report exactly with these section headings:

# Founder Briefing
# Startup Overview
# Strategic Evaluation
# Future Scenarios
# Key Risks
# Strategic Recommendations

Formatting requirements:
- In Strategic Evaluation, mention the overall score clearly
- In Future Scenarios, create 3 short subsections:
  ## Best-Case Scenario
  ## Realistic Scenario
  ## Worst-Case Scenario
- In Key Risks, use bullet points
- In Strategic Recommendations, use numbered action steps
- Keep the tone suitable for a founder preparing to make a decision

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
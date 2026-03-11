from utils.gemini_client import get_gemini_client


def generate_report(structured, scoring, scenarios, risks, recommendations, analysis_mode):
    client = get_gemini_client()

    tone_map = {
        "Founder": """
Write like a high-level startup advisor briefing a founder.
Be sharp, constructive, and strategic.
""",
        "Investor": """
Write like an investor memo.
Be analytical, commercially minded, and skeptical.
""",
        "Brutal": """
Write like a brutally honest partner reviewing a weak or uncertain startup.
Be direct, cutting, and unsentimental.
Do not soften obvious weaknesses.
Still be useful, intelligent, and professionally written.
"""
    }

    tone_instruction = tone_map.get(analysis_mode, tone_map["Founder"])

    prompt = f"""
You are a high-level startup strategy advisor.

Write a serious startup briefing memo.

Mode:
{analysis_mode}

Tone instructions:
{tone_instruction}

Writing requirements:
- Professional
- Concise but high-signal
- Do not sound like a chatbot
- Do not mention JSON, structured data, or "provided information"
- Focus on business truth, not motivational fluff
- Make the report feel like an internal strategy memo
- Open with 2-3 sentences framing the startup as a real business under evaluation

Structure the report exactly with these headings:

# Executive Brief
# Business Overview
# Strategic Assessment
# Future Outlook
# Core Risks
# Recommended Actions

Extra formatting rules:
- In Strategic Assessment, mention the overall score naturally
- In Future Outlook, use these subheadings:
  ## Best-Case
  ## Realistic Case
  ## Worst-Case
- In Core Risks, use bullet points
- In Recommended Actions, use numbered action steps
- Keep sentences crisp
- Avoid repetitive phrasing

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
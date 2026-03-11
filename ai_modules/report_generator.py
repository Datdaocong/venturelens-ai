from utils.gemini_client import get_gemini_client


def generate_report(structured, scoring, scenarios, risks, recommendations, analysis_mode):
    client = get_gemini_client()

    tone_map = {
        "Founder": """
Write like a sharp startup advisor speaking directly to a founder.
Be constructive, practical, and strategically clear.
The founder should feel guided, not comforted.
""",
        "Investor": """
Write like an internal investor memo.
Be analytical, commercially grounded, and skeptical.
Focus on whether this is actually a venture-backable business.
""",
        "Brutal": """
Write like a brutally honest partner reviewing a startup that may be fooling itself.
Be incisive, unsentimental, and hard to impress.
Attack weak assumptions, shallow differentiation, lazy market thinking, and feature-not-company ideas.
Do not be mean for style points; be sharp because precision matters.
"""
    }

    tone_instruction = tone_map.get(analysis_mode, tone_map["Founder"])

    prompt = f"""
You are an elite startup strategist.

Write a memo that feels like a serious human assessment, not an AI summary.

Mode:
{analysis_mode}

Tone instructions:
{tone_instruction}

Non-negotiable writing rules:
- Do not sound robotic
- Do not repeat the input mechanically
- Do not mention JSON, structured data, or "based on the analysis"
- Every section must contain a real judgment, not just description
- Use strong, clean business language
- Vary sentence length
- Avoid generic startup clichés
- Make the report feel like it was written by someone who has seen many startups succeed and fail
- If something is weak, say it clearly
- If something is promising, explain exactly why
- Start with a sharp opening paragraph that frames the startup's core bet in plain English
- Write as if speaking to an ambitious founder with limited time and limited room for self-deception
- Prefer insight over completeness

Write the report using exactly these headings:

# Executive Take
# What This Startup Is Really Betting On
# Why This Could Work
# Why This Could Break
# What the Next 12 Months Probably Look Like
# What You Should Do Now

Formatting rules:
- Under "What the Next 12 Months Probably Look Like", include these exact subheadings:
  ## Best-Case
  ## Realistic Case
  ## Worst-Case
- Under "Why This Could Break", use bullet points
- Under "What You Should Do Now", use numbered action steps
- Keep it tight, sharp, and high-signal

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
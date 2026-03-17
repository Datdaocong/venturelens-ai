from __future__ import annotations


def generate_recommendations(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict,
    risks: dict,
    similar_startups: list[dict] | None = None,
    retrieval_summary: dict | None = None,
) -> dict:
    retrieval_summary = retrieval_summary or {}

    overall = float(scoring.get("overall_score", 5))
    score_dict = scoring.get("scores", {})
    competition = float(score_dict.get("competitive_pressure", 5))
    feasibility = float(score_dict.get("feasibility", 5))
    market = float(score_dict.get("market_attractiveness", 5))

    top_outcomes = retrieval_summary.get("top_outcomes", [])
    top_industries = retrieval_summary.get("top_industries", [])

    next_steps = [
        "Narrow the initial ICP to a more specific customer segment with a clear, urgent pain point.",
        "Review the top 3–5 similar startups to identify where they won, where they failed, and where your wedge can be stronger.",
    ]

    if competition < 5:
        next_steps.append("Define a sharper differentiation angle instead of positioning too broadly.")

    if feasibility < 5:
        next_steps.append("Reduce MVP scope to one workflow so you can validate value faster and execute more efficiently.")

    if market < 5:
        next_steps.append("Prioritize customer interviews and willingness-to-pay validation before expanding the product scope.")

    mvp_focus = (
        "Focus on a narrow, high-frequency use case that creates measurable value quickly."
    )

    validation_focus = (
        "Validate pain intensity, urgency, willingness to pay, and why users would choose your product over current alternatives."
    )

    strategic_note = (
        f"The current peer cluster is concentrated in: {', '.join(top_industries) if top_industries else 'unknown industries'}. "
        f"Common peer outcomes: {', '.join(top_outcomes) if top_outcomes else 'unknown'}."
    )

    if overall >= 7:
        verdict = "Promising, but execution discipline still matters."
    elif overall >= 5:
        verdict = "Potentially viable, but it needs sharper positioning and stronger validation."
    else:
        verdict = "High-risk unless the scope is narrowed significantly and demand is validated early."

    return {
        "verdict": verdict,
        "next_steps": next_steps,
        "mvp_focus": mvp_focus,
        "validation_focus": validation_focus,
        "strategic_note": strategic_note,
    }
from __future__ import annotations


def analyze_risks(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict | None = None,
    similar_startups: list[dict] | None = None,
) -> dict:
    similar_startups = similar_startups or []
    scores = scoring.get("scores", {})

    risks = []

    market_score = scores.get("market_attractiveness", 5)
    feasibility = scores.get("feasibility", 5)
    competition = scores.get("competitive_pressure", 5)
    signal_strength = scores.get("signal_strength", 5)

    if competition < 4:
        risks.append("The comparable startup cluster appears crowded, so differentiation may be difficult.")

    if feasibility < 5:
        risks.append("Execution may be difficult because similar startups needed significant time or funding to mature.")

    if market_score < 5:
        risks.append("Comparable startups show weak market signals, suggesting uncertain demand or poor category dynamics.")

    if signal_strength < 5:
        risks.append("The retrieval evidence is weak, so conclusions should be treated cautiously.")

    if not risks:
        risks.append("No major red flags from the peer set, but execution and differentiation still matter.")

    return {
        "top_risks": risks,
        "risk_level": "high" if len(risks) >= 3 else "medium" if len(risks) == 2 else "low",
    }
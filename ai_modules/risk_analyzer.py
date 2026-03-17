from __future__ import annotations


def analyze_risks(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict | None = None,
    similar_startups: list[dict] | None = None,
    retrieval_summary: dict | None = None,
) -> dict:
    similar_startups = similar_startups or []
    retrieval_summary = retrieval_summary or {}
    scores = scoring.get("scores", {})

    risks = []
    evidence = []

    market_score = float(scores.get("market_attractiveness", 5))
    feasibility = float(scores.get("feasibility", 5))
    competitive_pressure = float(scores.get("competitive_pressure", 5))
    signal_strength = float(scores.get("signal_strength", 5))

    peer_count = int(retrieval_summary.get("peer_count", len(similar_startups)))
    avg_success = float(retrieval_summary.get("avg_success_score", 0))
    avg_rounds = float(retrieval_summary.get("avg_funding_round_count", 0))
    acquisition_rate = float(retrieval_summary.get("acquisition_rate", 0))
    ipo_rate = float(retrieval_summary.get("ipo_rate", 0))
    top_outcomes = retrieval_summary.get("top_outcomes", [])

    if competitive_pressure < 4:
        risks.append("The comparable startup cluster appears crowded, so differentiation may be difficult.")
        evidence.append("Competitive pressure is high in the retrieved peer set.")

    if market_score < 5:
        risks.append("Peer startups show weak market signals, which may indicate uncertain demand.")
        evidence.append(f"Average peer success score is only {avg_success:.2f}.")

    if feasibility < 5:
        risks.append("Execution may be difficult because similar startups often required multiple funding rounds to mature.")
        evidence.append(f"Average peer funding rounds: {avg_rounds:.2f}.")

    if signal_strength < 5:
        risks.append("The evidence signal is not yet strong, so conclusions should be treated with caution.")
        evidence.append("Similarity signal strength is relatively weak.")

    if peer_count >= 5 and acquisition_rate == 0 and ipo_rate == 0:
        risks.append("The peer cluster shows weak exit patterns, suggesting limited upside.")
        evidence.append("No strong acquisition or IPO pattern is visible in the peer set.")

    if "closed" in top_outcomes:
        risks.append("A meaningful share of comparable startups appear to end with weak outcomes or shutdowns.")
        evidence.append(f"Common peer outcomes include: {', '.join(top_outcomes)}.")

    if not risks:
        risks.append("No major red flags were found in the peer set, but execution and differentiation remain critical.")
        evidence.append("Peer evidence looks reasonably healthy.")

    risk_level = "Low"
    if len(risks) >= 4:
        risk_level = "High"
    elif len(risks) >= 2:
        risk_level = "Medium"

    return {
        "risk_level": risk_level,
        "top_risks": risks,
        "evidence": evidence,
    }
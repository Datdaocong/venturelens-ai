from __future__ import annotations


def simulate_future_scenarios(
    structured_idea: dict,
    scoring: dict,
    similar_startups: list[dict] | None = None,
    retrieval_summary: dict | None = None,
) -> dict:
    retrieval_summary = retrieval_summary or {}

    overall = float(scoring.get("overall_score", 5))
    avg_success = float(retrieval_summary.get("avg_success_score", 0))
    avg_rounds = float(retrieval_summary.get("avg_funding_round_count", 0))
    acquisition_rate = float(retrieval_summary.get("acquisition_rate", 0))
    ipo_rate = float(retrieval_summary.get("ipo_rate", 0))
    top_outcomes = retrieval_summary.get("top_outcomes", [])

    if overall >= 7:
        optimistic = (
            "If the startup achieves sharp positioning and strong execution, it could follow the path of the strongest peers: "
            "early validation, initial traction, and eventual growth-stage momentum."
        )
    else:
        optimistic = (
            "In the best case, the startup can still find a focused niche, gain early traction, and prove clear user value."
        )

    realistic = (
        f"The most realistic path is a slower validation cycle. "
        f"Peer startups currently show an average success score of {avg_success:.2f} "
        f"and average funding rounds of {avg_rounds:.2f}, suggesting that product iteration and positioning will matter a lot."
    )

    if acquisition_rate > 0 or ipo_rate > 0:
        risky = (
            "In the downside case, the startup fails to differentiate, struggles to maintain traction, "
            "and never converts early attention into sustainable growth."
        )
    else:
        risky = (
            "In the downside case, the startup falls into the weaker outcome pattern of the cluster: "
            "unclear demand, weak scaling, and limited exit potential."
        )

    return {
        "optimistic": optimistic,
        "realistic": realistic,
        "risky": risky,
        "scenario_evidence": {
            "avg_success_score": avg_success,
            "avg_funding_round_count": avg_rounds,
            "acquisition_rate": acquisition_rate,
            "ipo_rate": ipo_rate,
            "top_outcomes": top_outcomes,
        },
    }
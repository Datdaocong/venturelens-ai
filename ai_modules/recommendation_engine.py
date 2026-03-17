from __future__ import annotations

from typing import Any, Dict, List


def generate_recommendations(
    user_idea: str,
    scoring: Dict[str, Any],
    risk: Dict[str, Any],
    peer_signals: Dict[str, Any],
) -> List[str]:
    recommendations: List[str] = []

    overall_score = float(scoring.get("overall_score", 0))
    risk_level = risk.get("risk_level", "Medium")
    failure_ratio = float(peer_signals.get("failure_ratio", 0))
    avg_similarity = float(peer_signals.get("avg_similarity", 0))
    dominant_industry = peer_signals.get("dominant_industry", "Unknown")

    recommendations.append("Validate the idea with 10-20 target users before building more features.")
    recommendations.append("Define one narrow customer segment and one specific painful problem to solve.")
    recommendations.append("Turn the current idea into a sharper MVP hypothesis with clear success metrics.")

    if dominant_industry != "Unknown":
        recommendations.append(
            f"Study peer patterns in the {dominant_industry} segment and identify what stronger startups did differently."
        )

    if avg_similarity < 0.20:
        recommendations.append(
            "Clarify the problem statement and positioning because the system found weak historical matches."
        )
    else:
        recommendations.append(
            "Use the retrieved similar startups as reference cases for feature scope, messaging, and go-to-market strategy."
        )

    if failure_ratio >= 0.50:
        recommendations.append(
            "Prioritize differentiation and retention strategy because peer failure rate is high."
        )

    if overall_score < 55:
        recommendations.append(
            "Start with a lightweight MVP and validation milestones before spending heavily on scaling."
        )
    else:
        recommendations.append(
            "Prepare a clearer go-to-market plan and collect early traction metrics that investors or judges can understand."
        )

    if risk_level == "High":
        recommendations.append(
            "Reduce scope and test one use case first to lower execution risk."
        )

    return recommendations
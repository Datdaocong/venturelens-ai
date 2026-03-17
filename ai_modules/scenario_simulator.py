from __future__ import annotations

from typing import Any, Dict


def simulate_scenarios(
    user_idea: str,
    scoring: Dict[str, Any],
    risk: Dict[str, Any],
    peer_signals: Dict[str, Any],
) -> Dict[str, str]:
    overall_score = float(scoring.get("overall_score", 0))
    risk_level = risk.get("risk_level", "Medium")
    success_ratio = float(peer_signals.get("success_ratio", 0))
    failure_ratio = float(peer_signals.get("failure_ratio", 0))
    avg_similarity = float(peer_signals.get("avg_similarity", 0))
    dominant_industry = peer_signals.get("dominant_industry", "Unknown")

    if overall_score >= 75 and risk_level == "Low":
        best_case = (
            f"The idea gains early traction in the {dominant_industry} segment, "
            "finds clear customer pain points, and reaches strong validation quickly."
        )
    elif overall_score >= 55:
        best_case = (
            "The idea reaches moderate traction after narrowing the target segment "
            "and improving go-to-market execution."
        )
    else:
        best_case = (
            "The idea only gains traction after major repositioning, clearer differentiation, "
            "or a smaller initial market focus."
        )

    if success_ratio >= 0.50 and avg_similarity >= 0.25:
        base_case = (
            "The startup has a realistic chance of building an MVP with usable traction, "
            "but growth will depend on disciplined execution and validation."
        )
    elif failure_ratio > success_ratio:
        base_case = (
            "The startup may struggle to convert interest into consistent traction unless it avoids "
            "the same mistakes seen in weaker peer companies."
        )
    else:
        base_case = (
            "The startup may reach early validation, but commercial success remains uncertain."
        )

    if risk_level == "High":
        worst_case = (
            "The startup fails to differentiate, shows weak validation, and faces early shutdown risk."
        )
    elif avg_similarity < 0.20:
        worst_case = (
            "The startup enters an unclear category with weak historical matches, making product-market fit hard to prove."
        )
    else:
        worst_case = (
            "The startup sees slow adoption, weak retention, and delayed monetization."
        )

    return {
        "best_case": best_case,
        "base_case": base_case,
        "worst_case": worst_case,
    }
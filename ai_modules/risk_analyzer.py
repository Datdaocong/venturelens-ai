from __future__ import annotations

from typing import Any, Dict, List


def analyze_risk(
    user_idea: str,
    similar_startups: List[Dict[str, Any]],
    scoring: Dict[str, Any],
    aggregated_signals: Dict[str, Any],
) -> Dict[str, Any]:
    failure_ratio = float(aggregated_signals.get("failure_ratio", 0))
    success_ratio = float(aggregated_signals.get("success_ratio", 0))
    avg_similarity = float(aggregated_signals.get("avg_similarity", 0))
    avg_success_score = float(aggregated_signals.get("avg_success_score", 0))
    num_peers = int(aggregated_signals.get("num_peers", 0))
    overall_score = float(scoring.get("overall_score", 50))

    risk_flags: List[str] = []
    risk_breakdown: Dict[str, str] = {}

    if num_peers < 3:
        risk_flags.append("Limited peer evidence in dataset")
        risk_breakdown["evidence_risk"] = "Few similar startups were retrieved, so confidence is lower."

    if avg_similarity < 0.20:
        risk_flags.append("Weak match with known startup patterns")
        risk_breakdown["retrieval_risk"] = "Retrieved peers are not strongly similar to the user idea."

    if failure_ratio >= 0.50:
        risk_flags.append("High failure rate among similar startups")
        risk_breakdown["market_risk"] = "Many similar startups in the dataset ended with failed outcomes."

    if avg_success_score < 45:
        risk_flags.append("Low average peer success score")
        risk_breakdown["quality_risk"] = "Peer group itself has weak historical performance."

    if overall_score < 45:
        risk_flags.append("Low evidence-backed viability score")
        risk_breakdown["viability_risk"] = "Combined scoring signals suggest weak startup viability."

    if success_ratio >= 0.60 and failure_ratio <= 0.20 and avg_similarity >= 0.30:
        mitigating_factors = [
            "Peer group includes a healthy share of successful examples",
            "Retrieved peers have reasonable similarity to the current idea",
        ]
    else:
        mitigating_factors = [
            "More validation may improve confidence in the idea",
            "Sharper positioning could separate the idea from weaker peers",
        ]

    if len(risk_flags) >= 4:
        risk_level = "High"
    elif len(risk_flags) >= 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_level": risk_level,
        "risk_flags": risk_flags,
        "risk_breakdown": risk_breakdown,
        "mitigating_factors": mitigating_factors,
    }
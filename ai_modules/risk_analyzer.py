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
    max_similarity = float(aggregated_signals.get("max_similarity", 0))
    avg_success_score = float(aggregated_signals.get("avg_success_score", 0))
    num_peers = int(aggregated_signals.get("num_peers", 0))
    overall_score = float(scoring.get("overall_score", 50))

    risk_flags: List[str] = []
    risk_breakdown: Dict[str, str] = {}

    if num_peers < 3:
        risk_flags.append("Limited peer evidence in dataset")
        risk_breakdown["evidence_risk"] = "Too few similar startups were retrieved."

    if avg_similarity < 0.15:
        risk_flags.append("Very weak match with known startup patterns")
        risk_breakdown["retrieval_risk"] = "Retrieved peers are only weakly related to the idea."
    elif avg_similarity < 0.25:
        risk_flags.append("Weak match with known startup patterns")
        risk_breakdown["retrieval_risk"] = "Similarity to peer startups is limited."

    if max_similarity < 0.25:
        risk_flags.append("No strong nearest-neighbor match found")
        risk_breakdown["nearest_peer_risk"] = "The idea lacks a convincing close peer in the dataset."

    if failure_ratio >= 0.50:
        risk_flags.append("High failure rate among similar startups")
        risk_breakdown["market_risk"] = "Many similar startups ended in failed outcomes."

    if avg_success_score < 45:
        risk_flags.append("Low average peer success score")
        risk_breakdown["quality_risk"] = "The peer group has weak historical performance."

    if overall_score < 45:
        risk_flags.append("Low evidence-backed viability score")
        risk_breakdown["viability_risk"] = "Combined signals suggest weak viability."

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
        "mitigating_factors": [
            "Sharper positioning may improve retrieval quality",
            "Better validation with real target users could reduce uncertainty",
        ],
    }
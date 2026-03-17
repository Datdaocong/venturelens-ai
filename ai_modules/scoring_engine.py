from __future__ import annotations

from typing import Any, Dict, List


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _compute_funding_score(avg_funding: float) -> float:
    """
    Scale funding proxy to 0-100.
    Assumption: 10M+ is already strong enough to saturate score.
    """
    if avg_funding <= 0:
        return 0.0
    return _clamp((avg_funding / 10_000_000) * 100)


def _compute_similarity_confidence(avg_similarity: float, max_similarity: float) -> float:
    score = (avg_similarity * 70) + (max_similarity * 30)
    return _clamp(score * 100)


def _compute_percentile_proxy(
    avg_peer_success_score: float,
    peer_success_ratio: float,
    avg_similarity: float,
) -> float:
    percentile = (
        avg_peer_success_score * 0.55
        + peer_success_ratio * 100 * 0.30
        + avg_similarity * 100 * 0.15
    )
    return _clamp(percentile)


def score_startup_idea(
    user_idea: str,
    similar_startups: List[Dict[str, Any]],
    aggregated_signals: Dict[str, Any],
) -> Dict[str, Any]:
    avg_success = float(aggregated_signals.get("avg_success_score", 50))
    success_ratio = float(aggregated_signals.get("success_ratio", 0.5))
    failure_ratio = float(aggregated_signals.get("failure_ratio", 0.2))
    avg_similarity = float(aggregated_signals.get("avg_similarity", 0.0))
    max_similarity = float(aggregated_signals.get("max_similarity", 0.0))
    avg_funding = float(aggregated_signals.get("avg_funding", 0.0))
    num_peers = int(aggregated_signals.get("num_peers", 0))

    funding_score = _compute_funding_score(avg_funding)
    similarity_confidence = _compute_similarity_confidence(avg_similarity, max_similarity)
    percentile_proxy = _compute_percentile_proxy(avg_success, success_ratio, avg_similarity)

    peer_signal_strength = _clamp(
        avg_success * 0.45
        + success_ratio * 100 * 0.25
        + similarity_confidence * 0.20
        + funding_score * 0.10
    )

    evidence_quality = _clamp(
        similarity_confidence * 0.70
        + min(num_peers / 5, 1.0) * 100 * 0.30
    )

    risk_penalty = _clamp(
        failure_ratio * 100 * 0.70
        + (20 if num_peers < 3 else 0)
    )

    overall_score = _clamp(
        peer_signal_strength * 0.70
        + percentile_proxy * 0.20
        + evidence_quality * 0.10
        - risk_penalty * 0.25
    )

    if overall_score >= 75:
        verdict = "Strong"
    elif overall_score >= 55:
        verdict = "Moderate"
    else:
        verdict = "Weak"

    return {
        "overall_score": round(overall_score, 2),
        "verdict": verdict,
        "peer_signal_strength": round(peer_signal_strength, 2),
        "evidence_quality": round(evidence_quality, 2),
        "similarity_confidence": round(similarity_confidence, 2),
        "percentile_proxy": round(percentile_proxy, 2),
        "risk_penalty": round(risk_penalty, 2),
        "avg_peer_success_score": round(avg_success, 2),
        "peer_success_ratio": round(success_ratio, 2),
        "peer_failure_ratio": round(failure_ratio, 2),
        "avg_similarity": round(avg_similarity, 4),
        "max_similarity": round(max_similarity, 4),
        "avg_funding": round(avg_funding, 2),
        "num_peers": num_peers,
    }
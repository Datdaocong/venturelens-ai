from __future__ import annotations

from typing import Any, Dict, List


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score_startup_idea(
    user_idea: str,
    similar_startups: List[Dict[str, Any]],
    aggregated_signals: Dict[str, Any],
) -> Dict[str, Any]:
    avg_success = float(aggregated_signals.get("avg_success_score", 0.0))
    success_ratio = float(aggregated_signals.get("success_ratio", 0.0))
    failure_ratio = float(aggregated_signals.get("failure_ratio", 0.0))
    avg_similarity = float(aggregated_signals.get("avg_similarity", 0.0))
    max_similarity = float(aggregated_signals.get("max_similarity", 0.0))
    avg_funding = float(aggregated_signals.get("avg_funding", 0.0))
    num_peers = int(aggregated_signals.get("num_peers", 0))

    # 1) Core evidence scores
    similarity_confidence = _clamp((avg_similarity * 0.7 + max_similarity * 0.3) * 100)
    peer_quality = _clamp(avg_success)
    peer_outcome_strength = _clamp((success_ratio - failure_ratio + 1) * 50)  # maps roughly to 0-100

    # 2) Evidence quality should punish weak retrieval
    if num_peers >= 5:
        peer_count_score = 100
    elif num_peers == 4:
        peer_count_score = 80
    elif num_peers == 3:
        peer_count_score = 60
    elif num_peers == 2:
        peer_count_score = 35
    elif num_peers == 1:
        peer_count_score = 15
    else:
        peer_count_score = 0

    evidence_quality = _clamp(
        similarity_confidence * 0.75 +
        peer_count_score * 0.25
    )

    # 3) Tiny funding effect only
    funding_score = 0.0
    if avg_funding > 0:
        funding_score = min(avg_funding / 20_000_000 * 100, 100)

    # 4) Raw score is intentionally conservative
    raw_score = (
        peer_quality * 0.35 +
        similarity_confidence * 0.30 +
        peer_outcome_strength * 0.20 +
        evidence_quality * 0.10 +
        funding_score * 0.05
    )

    # 5) Strong penalties
    penalty = 0.0

    if avg_similarity < 0.15:
        penalty += 30
    elif avg_similarity < 0.25:
        penalty += 18
    elif avg_similarity < 0.35:
        penalty += 8

    if max_similarity < 0.25:
        penalty += 12

    if failure_ratio >= 0.60:
        penalty += 18
    elif failure_ratio >= 0.40:
        penalty += 10

    if num_peers < 3:
        penalty += 15

    # 6) Gating rule: weak retrieval can never score too high
    capped_score = raw_score - penalty

    if avg_similarity < 0.15:
        capped_score = min(capped_score, 35)
    elif avg_similarity < 0.25:
        capped_score = min(capped_score, 50)
    elif avg_similarity < 0.35:
        capped_score = min(capped_score, 65)

    if num_peers < 3:
        capped_score = min(capped_score, 55)

    overall_score = _clamp(round(capped_score, 2))

    if overall_score >= 75:
        verdict = "Strong"
    elif overall_score >= 55:
        verdict = "Moderate"
    else:
        verdict = "Weak"

    return {
        "overall_score": overall_score,
        "verdict": verdict,
        "peer_quality": round(peer_quality, 2),
        "peer_outcome_strength": round(peer_outcome_strength, 2),
        "similarity_confidence": round(similarity_confidence, 2),
        "evidence_quality": round(evidence_quality, 2),
        "funding_score": round(funding_score, 2),
        "penalty": round(penalty, 2),
        "avg_peer_success_score": round(avg_success, 2),
        "peer_success_ratio": round(success_ratio, 2),
        "peer_failure_ratio": round(failure_ratio, 2),
        "avg_similarity": round(avg_similarity, 4),
        "max_similarity": round(max_similarity, 4),
        "avg_funding": round(avg_funding, 2),
        "num_peers": num_peers,
    }
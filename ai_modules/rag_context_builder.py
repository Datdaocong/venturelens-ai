from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from ai_modules.similarity_bridge import retrieve_similar_startups


SUCCESS_LABELS = {"success", "successful", "acquired", "ipo", "exit"}
FAILURE_LABELS = {"failed", "shutdown", "dead", "closed"}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _safe_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    text = str(value).strip()
    return text if text else default


def _normalize_outcome_label(label: Any) -> str:
    return _safe_text(label, "unknown").lower()


def _build_startup_item(row: pd.Series) -> Dict[str, Any]:
    return {
        "name": _safe_text(row.get("name"), "Unknown Startup"),
        "description": _safe_text(row.get("description"), ""),
        "industry": _safe_text(row.get("industry"), "Unknown"),
        "funding": _safe_float(
            row.get("funding", row.get("total_funding_usd", 0.0)),
            0.0,
        ),
        "success_score": _safe_float(row.get("success_score"), 0.0),
        "outcome_label": _safe_text(row.get("outcome_label"), "unknown"),
        "similarity_score": _safe_float(
            row.get("similarity_score", row.get("similarity", 0.0)),
            0.0,
        ),
    }

def _aggregate_signals(similar_startups: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not similar_startups:
        return {
            "num_peers": 0,
            "avg_success_score": 0.0,
            "avg_funding": 0.0,
            "avg_similarity": 0.0,
            "max_similarity": 0.0,
            "success_ratio": 0.0,
            "failure_ratio": 0.0,
            "outcome_mix": {"success": 0, "failure": 0, "unknown": 0},
            "industry_distribution": {},
            "dominant_industry": "Unknown",
        }

    n = len(similar_startups)
    avg_success_score = sum(x["success_score"] for x in similar_startups) / n
    avg_funding = sum(x["funding"] for x in similar_startups) / n
    avg_similarity = sum(x["similarity_score"] for x in similar_startups) / n
    max_similarity = max(x["similarity_score"] for x in similar_startups)

    success_count = 0
    failure_count = 0
    unknown_count = 0
    industry_distribution: Dict[str, int] = {}

    for item in similar_startups:
        outcome = _normalize_outcome_label(item.get("outcome_label"))
        if outcome in SUCCESS_LABELS:
            success_count += 1
        elif outcome in FAILURE_LABELS:
            failure_count += 1
        else:
            unknown_count += 1

        industry = item.get("industry", "Unknown") or "Unknown"
        industry_distribution[industry] = industry_distribution.get(industry, 0) + 1

    dominant_industry = max(industry_distribution, key=industry_distribution.get)

    return {
        "num_peers": n,
        "avg_success_score": round(avg_success_score, 2),
        "avg_funding": round(avg_funding, 2),
        "avg_similarity": round(avg_similarity, 4),
        "max_similarity": round(max_similarity, 4),
        "success_ratio": round(success_count / n, 2),
        "failure_ratio": round(failure_count / n, 2),
        "outcome_mix": {
            "success": success_count,
            "failure": failure_count,
            "unknown": unknown_count,
        },
        "industry_distribution": industry_distribution,
        "dominant_industry": dominant_industry,
    }


def _build_evidence_text(
    user_idea: str,
    similar_startups: List[Dict[str, Any]],
    aggregated_signals: Dict[str, Any],
) -> str:
    lines: List[str] = []

    lines.append("USER IDEA:")
    lines.append(user_idea.strip())
    lines.append("")
    lines.append("RETRIEVED SIMILAR STARTUPS FROM REAL DATA:")

    if not similar_startups:
        lines.append("No similar startups found in the dataset.")
    else:
        for i, s in enumerate(similar_startups, start=1):
            lines.append(
                f"{i}. {s['name']} | industry={s['industry']} | "
                f"success_score={s['success_score']} | funding={s['funding']} | "
                f"outcome={s['outcome_label']} | similarity={s['similarity_score']:.4f}"
            )
            if s["description"]:
                lines.append(f"   description: {s['description']}")

    lines.append("")
    lines.append("AGGREGATED PEER SIGNALS:")
    lines.append(f"- num_peers: {aggregated_signals.get('num_peers', 0)}")
    lines.append(f"- dominant_industry: {aggregated_signals.get('dominant_industry', 'Unknown')}")
    lines.append(f"- avg_success_score: {aggregated_signals.get('avg_success_score', 0)}")
    lines.append(f"- avg_funding: {aggregated_signals.get('avg_funding', 0)}")
    lines.append(f"- avg_similarity: {aggregated_signals.get('avg_similarity', 0)}")
    lines.append(f"- max_similarity: {aggregated_signals.get('max_similarity', 0)}")
    lines.append(f"- success_ratio: {aggregated_signals.get('success_ratio', 0)}")
    lines.append(f"- failure_ratio: {aggregated_signals.get('failure_ratio', 0)}")

    outcome_mix = aggregated_signals.get("outcome_mix", {})
    lines.append(
        f"- outcome_mix: success={outcome_mix.get('success', 0)}, "
        f"failure={outcome_mix.get('failure', 0)}, "
        f"unknown={outcome_mix.get('unknown', 0)}"
    )

    industry_distribution = aggregated_signals.get("industry_distribution", {})
    if industry_distribution:
        lines.append("- industry_distribution:")
        for industry, count in sorted(
            industry_distribution.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            lines.append(f"  - {industry}: {count}")

    return "\n".join(lines)


def build_rag_context(user_idea: str, top_k: int = 5) -> Dict[str, Any]:
    df_similar = retrieve_similar_startups(user_idea, top_k=top_k)

    if df_similar is None or df_similar.empty:
        aggregated_signals = _aggregate_signals([])
        return {
            "similar_startups": [],
            "aggregated_signals": aggregated_signals,
            "evidence_text": _build_evidence_text(user_idea, [], aggregated_signals),
        }

    similar_startups = [_build_startup_item(row) for _, row in df_similar.iterrows()]
    aggregated_signals = _aggregate_signals(similar_startups)
    evidence_text = _build_evidence_text(
        user_idea=user_idea,
        similar_startups=similar_startups,
        aggregated_signals=aggregated_signals,
    )

    return {
        "similar_startups": similar_startups,
        "aggregated_signals": aggregated_signals,
        "evidence_text": evidence_text,
    }
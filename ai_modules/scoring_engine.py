from __future__ import annotations

import pandas as pd


def _clamp(value: float, low: float = 0.0, high: float = 10.0) -> float:
    return max(low, min(high, value))


def score_startup(structured_idea: dict, similar_startups: list[dict]) -> dict:
    if not similar_startups:
        return {
            "overall_score": 5.0,
            "scores": {
                "market_attractiveness": 5.0,
                "feasibility": 5.0,
                "competitive_pressure": 5.0,
                "signal_strength": 5.0,
            },
            "summary": "No strong peer evidence was found, so scoring is neutral.",
            "evidence": {},
        }

    df = pd.DataFrame(similar_startups)

    for col in [
        "success_score",
        "funding_round_count",
        "total_funding_usd",
        "has_acquisition",
        "has_ipo",
        "similarity",
    ]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    avg_success = float(df["success_score"].mean())
    avg_rounds = float(df["funding_round_count"].mean())
    avg_similarity = float(df["similarity"].mean())
    exit_rate = float((df["has_acquisition"] + df["has_ipo"] > 0).mean())

    market_attractiveness = _clamp(avg_success)
    feasibility = _clamp(3 + avg_rounds * 1.2)
    competitive_pressure = _clamp(10 - (len(df) * 0.8))
    signal_strength = _clamp(avg_similarity * 10 + exit_rate * 2)

    overall = round(
        (market_attractiveness * 0.35)
        + (feasibility * 0.25)
        + (competitive_pressure * 0.20)
        + (signal_strength * 0.20),
        2,
    )

    scores = {
        "market_attractiveness": round(market_attractiveness, 2),
        "feasibility": round(feasibility, 2),
        "competitive_pressure": round(competitive_pressure, 2),
        "signal_strength": round(signal_strength, 2),
    }

    summary = (
        f"This score is grounded in {len(df)} similar startups. "
        f"Peers show an average success score of {avg_success:.2f}, "
        f"average funding rounds of {avg_rounds:.2f}, "
        f"and an exit rate of {exit_rate:.2f}."
    )

    return {
        "overall_score": overall,
        "scores": scores,
        "summary": summary,
        "evidence": {
            "peer_count": int(len(df)),
            "avg_success_score": round(avg_success, 2),
            "avg_funding_round_count": round(avg_rounds, 2),
            "avg_similarity": round(avg_similarity, 4),
            "exit_rate": round(exit_rate, 2),
        },
    }
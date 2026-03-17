from __future__ import annotations

from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _risk_to_safety_score(risk_level: str) -> float:
    risk_level = str(risk_level).strip().lower()

    if risk_level == "low":
        return 85.0
    if risk_level == "medium":
        return 55.0
    if risk_level == "high":
        return 25.0
    return 50.0


def build_radar_metrics(scoring: Dict, risk: Dict) -> pd.DataFrame:
    overall_score = _clamp(float(scoring.get("overall_score", 0)))
    similarity_confidence = _clamp(float(scoring.get("similarity_confidence", 0)))
    peer_quality = _clamp(float(scoring.get("peer_quality", 0)))
    evidence_quality = _clamp(float(scoring.get("evidence_quality", 0)))
    risk_safety = _clamp(_risk_to_safety_score(risk.get("risk_level", "Medium")))

    data = [
        {"metric": "Viability", "value": overall_score},
        {"metric": "Retrieval Strength", "value": similarity_confidence},
        {"metric": "Peer Quality", "value": peer_quality},
        {"metric": "Evidence Depth", "value": evidence_quality},
        {"metric": "Risk Control", "value": risk_safety},
    ]

    return pd.DataFrame(data)


def create_radar_figure(scoring: Dict, risk: Dict) -> go.Figure:
    radar_df = build_radar_metrics(scoring, risk)

    categories: List[str] = radar_df["metric"].tolist()
    values: List[float] = radar_df["value"].tolist()

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            name="VentureLens Analysis",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
            )
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig
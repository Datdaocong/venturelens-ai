from __future__ import annotations

from typing import Any, Dict

from ai_modules.rag_context_builder import build_rag_context
from ai_modules.scoring_engine import score_startup_idea
from ai_modules.risk_analyzer import analyze_risk
from ai_modules.scenario_simulator import simulate_scenarios
from ai_modules.recommendation_engine import generate_recommendations
from ai_modules.report_generator import generate_final_report


def run_full_analysis(user_idea: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Main VentureLens pipeline:
    User Idea -> Retrieval -> RAG Context -> Scoring -> Risk -> Scenarios -> Recommendations -> Final Report
    """

    rag_context = build_rag_context(user_idea=user_idea, top_k=top_k)
    similar_startups = rag_context.get("similar_startups", [])
    aggregated_signals = rag_context.get("aggregated_signals", {})

    scoring = score_startup_idea(
        user_idea=user_idea,
        similar_startups=similar_startups,
        aggregated_signals=aggregated_signals,
    )

    risk = analyze_risk(
        user_idea=user_idea,
        similar_startups=similar_startups,
        scoring=scoring,
        aggregated_signals=aggregated_signals,
    )

    scenarios = simulate_scenarios(
        user_idea=user_idea,
        scoring=scoring,
        risk=risk,
        peer_signals=aggregated_signals,
    )

    recommendations = generate_recommendations(
        user_idea=user_idea,
        scoring=scoring,
        risk=risk,
        peer_signals=aggregated_signals,
    )

    report = generate_final_report(
        user_idea=user_idea,
        rag_context=rag_context,
        scoring=scoring,
        risk=risk,
        scenarios=scenarios,
        recommendations=recommendations,
    )

    return {
        "user_idea": user_idea,
        "rag_context": rag_context,
        "similar_startups": similar_startups,
        "aggregated_signals": aggregated_signals,
        "scoring": scoring,
        "risk": risk,
        "scenarios": scenarios,
        "recommendations": recommendations,
        "report": report,
    }
from __future__ import annotations

from ai_modules.idea_structurer import structure_startup_idea
from ai_modules.similarity_bridge import retrieve_similar_startups, summarize_similar_startups
from ai_modules.scoring_engine import score_startup
from ai_modules.risk_analyzer import analyze_risks
from ai_modules.scenario_simulator import simulate_future_scenarios
from ai_modules.recommendation_engine import generate_recommendations
from ai_modules.report_generator import generate_report


def run_full_analysis(user_idea: str) -> dict:
    structured_idea = structure_startup_idea(user_idea)

    similar_startups = retrieve_similar_startups(user_idea, top_k=5)
    retrieval_summary = summarize_similar_startups(similar_startups)

    scoring = score_startup(structured_idea, similar_startups)
    scenarios = simulate_future_scenarios(structured_idea, scoring, similar_startups)
    risks = analyze_risks(structured_idea, scoring, scenarios, similar_startups)
    recommendations = generate_recommendations(
        structured_idea,
        scoring,
        scenarios,
        risks,
        similar_startups,
    )

    report = generate_report(
        structured_idea,
        scoring,
        scenarios,
        risks,
        recommendations,
        similar_startups,
        retrieval_summary,
    )

    return {
        "structured_idea": structured_idea,
        "similar_startups": similar_startups,
        "retrieval_summary": retrieval_summary,
        "scoring": scoring,
        "scenarios": scenarios,
        "risks": risks,
        "recommendations": recommendations,
        "report": report,
    }
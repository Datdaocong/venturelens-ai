from ai_modules.idea_structurer import structure_startup_idea
from ai_modules.similarity_bridge import retrieve_similar_startups
from ai_modules.scoring_engine import score_startup
from ai_modules.risk_analyzer import analyze_risks
from ai_modules.recommendation_engine import generate_recommendations
from ai_modules.scenario_simulator import simulate_future_scenarios
from ai_modules.report_generator import generate_report


def run_full_analysis(user_idea):

    structured = structure_startup_idea(user_idea)

    similar = retrieve_similar_startups(user_idea, top_k=5)

    scoring = score_startup(structured, similar)

    scenarios = simulate_future_scenarios(structured, scoring)

    risks = analyze_risks(structured, scoring, scenarios)

    recommendations = generate_recommendations(
        structured,
        scoring,
        scenarios,
        risks
    )

    report = generate_report(
        structured,
        scoring,
        scenarios,
        risks,
        recommendations,
        similar
    )

    return {
        "structured_idea": structured,
        "similar_startups": similar,
        "scoring": scoring,
        "scenarios": scenarios,
        "risks": risks,
        "recommendations": recommendations,
        "report": report
    }
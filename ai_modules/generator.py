def generate_brief(idea_profile: dict, scores: dict) -> str:
    sectors = ", ".join(idea_profile.get("sectors", []))
    models = ", ".join(idea_profile.get("business_models", []))

    return (
        f"This startup idea appears to operate in {sectors} "
        f"with a business model leaning toward {models}. "
        f"The current overall viability score is {scores['overall']}/10, "
        f"suggesting a concept with promising signals but requiring sharper execution strategy."
    )


def generate_risk_flags(scores: dict) -> list[str]:
    risks = []

    if scores["execution_difficulty"] >= 8:
        risks.append("Execution may be technically or operationally difficult.")
    if scores["differentiation"] <= 5:
        risks.append("The idea may face strong competition from similar existing startups.")
    if scores["monetization_clarity"] <= 5:
        risks.append("Revenue model is not yet clearly defined.")
    if scores["market_attractiveness"] <= 5:
        risks.append("Market pull may not be strong enough without tighter positioning.")

    if not risks:
        risks.append("No critical red flags, but validation with real users is still needed.")

    return risks


def generate_future_scenarios(scores: dict) -> list[str]:
    overall = scores["overall"]

    if overall >= 8:
        return [
            "Best case: gains early traction in a fast-growing niche and becomes investor-attractive.",
            "Base case: finds a usable niche but needs stronger differentiation to scale.",
            "Worst case: execution delays allow competitors to capture the market first."
        ]

    if overall >= 6:
        return [
            "Best case: strong iteration improves positioning and unlocks product-market fit.",
            "Base case: works as a niche solution with moderate traction.",
            "Worst case: weak monetization and crowded competition limit adoption."
        ]

    return [
        "Best case: pivoting the concept reveals a more viable market angle.",
        "Base case: remains an interesting concept but struggles to convert users.",
        "Worst case: insufficient market demand prevents long-term growth."
    ]


def generate_peer_insights(similar_startups: list[dict]) -> list[str]:
    insights = []

    for peer in similar_startups[:3]:
        insights.append(
            f"{peer['startup_name']} shows overlap in {peer['industry']} "
            f"with similarity score {peer['similarity']}."
        )

    return insights


def build_analysis_report(
    idea_text: str,
    idea_profile: dict,
    similar_startups: list[dict],
    scores: dict
) -> dict:
    return {
        "idea_text": idea_text,
        "idea_profile": idea_profile,
        "scores": scores,
        "brief": generate_brief(idea_profile, scores),
        "risk_flags": generate_risk_flags(scores),
        "future_scenarios": generate_future_scenarios(scores),
        "similar_startups": similar_startups,
        "peer_insights": generate_peer_insights(similar_startups),
    }
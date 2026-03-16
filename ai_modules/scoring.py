def clamp_score(value: float, min_value: int = 1, max_value: int = 10) -> int:
    return max(min_value, min(int(round(value)), max_value))


def score_market_attractiveness(idea_profile: dict) -> int:
    sectors = idea_profile.get("sectors", [])
    score = 5

    if "ai" in sectors or "fintech" in sectors or "saas" in sectors:
        score += 2
    if "healthtech" in sectors or "edtech" in sectors:
        score += 1

    return clamp_score(score)


def score_execution_difficulty(idea_profile: dict) -> int:
    sectors = idea_profile.get("sectors", [])
    score = 5

    if "ai" in sectors:
        score += 2
    if "healthtech" in sectors or "fintech" in sectors:
        score += 2

    return clamp_score(score)


def score_differentiation(similar_startups: list[dict]) -> int:
    if not similar_startups:
        return 7

    top_similarity = similar_startups[0]["similarity"]

    if top_similarity >= 8:
        return 4
    if top_similarity >= 5:
        return 6
    return 8


def score_monetization_clarity(idea_profile: dict) -> int:
    models = idea_profile.get("business_models", [])
    score = 4

    if "subscription" in models:
        score += 3
    if "b2b" in models:
        score += 2
    if "transactional" in models or "marketplace" in models:
        score += 1

    return clamp_score(score)


def score_scalability(idea_profile: dict) -> int:
    sectors = idea_profile.get("sectors", [])
    models = idea_profile.get("business_models", [])
    score = 5

    if "saas" in sectors:
        score += 2
    if "b2b" in models:
        score += 1
    if "marketplace" in models:
        score += 1

    return clamp_score(score)


def compute_overall_score(scores: dict) -> int:
    values = list(scores.values())
    if not values:
        return 0
    return clamp_score(sum(values) / len(values))


def score_idea(idea_profile: dict, similar_startups: list[dict]) -> dict:
    scores = {
        "market_attractiveness": score_market_attractiveness(idea_profile),
        "execution_difficulty": score_execution_difficulty(idea_profile),
        "differentiation": score_differentiation(similar_startups),
        "monetization_clarity": score_monetization_clarity(idea_profile),
        "scalability": score_scalability(idea_profile),
    }
    scores["overall"] = compute_overall_score(scores)
    return scores
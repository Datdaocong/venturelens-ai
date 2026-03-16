import numpy as np

def score_startup(structured_idea, similar_startups):

    if len(similar_startups) == 0:
        return {
            "overall_score": 5,
            "scores": {},
            "summary": "No strong dataset evidence."
        }

    funding = [s["funding_round_count"] for s in similar_startups]
    exits = [s["has_acquisition"] + s["has_ipo"] for s in similar_startups]
    success = [s["success_score"] for s in similar_startups]

    market_score = np.mean(success) / 10
    competition_score = 10 - min(len(similar_startups), 10)

    feasibility = np.mean(funding)

    overall = (market_score + competition_score + feasibility) / 3

    return {
        "overall_score": round(overall, 2),
        "scores": {
            "market_attractiveness": round(market_score, 2),
            "competitive_pressure": round(competition_score, 2),
            "feasibility": round(feasibility, 2)
        },
        "summary": "Scoring based on similar startup signals."
    }
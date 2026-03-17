from __future__ import annotations


def simulate_future_scenarios(
    structured_idea: dict,
    scoring: dict,
    similar_startups: list[dict] | None = None,
) -> dict:
    similar_startups = similar_startups or []
    overall = scoring.get("overall_score", 5)

    if overall >= 7:
        base = "Peers suggest a promising market with reasonable execution potential."
    elif overall >= 5:
        base = "Peers suggest a viable but competitive opportunity."
    else:
        base = "Peers suggest a difficult path with meaningful market or execution risks."

    return {
        "optimistic": f"{base} With strong differentiation and execution, the startup could gain traction and attract early funding.",
        "realistic": f"{base} The most likely path is a slow validation cycle, focused niche adoption, and iterative refinement.",
        "risky": f"{base} Without clear differentiation or distribution, the startup may struggle to stand out and convert interest into growth.",
    }
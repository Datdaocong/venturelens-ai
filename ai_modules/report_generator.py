from __future__ import annotations


def generate_recommendations(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict,
    risks: dict,
    similar_startups: list[dict] | None = None,
) -> dict:
    similar_startups = similar_startups or []
    score = scoring.get("overall_score", 5)

    next_steps = [
        "Narrow the target customer segment and define a sharper initial wedge.",
        "Validate the pain point with real users before expanding the feature scope.",
        "Study the top similar startups and identify one concrete differentiation angle.",
    ]

    if score < 6:
        next_steps.append("Reduce product scope and focus on the smallest MVP that proves demand.")
    else:
        next_steps.append("Build an MVP around the strongest workflow or pain point first.")

    return {
        "next_steps": next_steps,
        "mvp_focus": "Start with a narrow, high-frequency use case that shows measurable value quickly.",
        "validation_focus": "Interview potential users, test willingness to pay, and compare against existing alternatives.",
    }
from __future__ import annotations

from typing import Any, Dict, List

def _format_scenario_block(label: str, scenario: Dict[str, Any]) -> str:
    warning_lines = scenario.get("warning_signs", [])
    warning_text = "\n".join(f"- {item}" for item in warning_lines) if warning_lines else "- None"

    return f"""
### {label}: {scenario.get("title", "N/A")}
**Description**  
{scenario.get("description", "N/A")}

**Why this could happen**  
{scenario.get("why_this_could_happen", "N/A")}

**Key trigger**  
{scenario.get("key_trigger", "N/A")}

**Warning signs**  
{warning_text}

**Strategic action**  
{scenario.get("strategic_action", "N/A")}
""".strip()

def _format_currency(value: float) -> str:
    try:
        return f"${value:,.0f}"
    except Exception:
        return str(value)


def _top_similar_summary(similar_startups: List[Dict[str, Any]], top_n: int = 3) -> str:
    if not similar_startups:
        return "No similar startups were retrieved from the dataset."

    lines = []
    for idx, item in enumerate(similar_startups[:top_n], start=1):
        lines.append(
            f"{idx}. {item.get('name', 'Unknown Startup')} "
            f"({item.get('industry', 'Unknown')}) | "
            f"similarity={item.get('similarity_score', 0):.3f} | "
            f"success_score={item.get('success_score', 0)} | "
            f"outcome={item.get('outcome_label', 'unknown')}"
        )
    return "\n".join(lines)


def _build_narrative_summary(
    user_idea: str,
    rag_context: Dict[str, Any],
    scoring: Dict[str, Any],
    risk: Dict[str, Any],
    scenarios: Dict[str, str],
    recommendations: List[str],
) -> str:
    signals = rag_context.get("aggregated_signals", {})
    similar_startups = rag_context.get("similar_startups", [])

    overall_score = scoring.get("overall_score", 0)
    verdict = scoring.get("verdict", "Unknown")
    risk_level = risk.get("risk_level", "Unknown")
    success_ratio = signals.get("success_ratio", 0)
    failure_ratio = signals.get("failure_ratio", 0)
    avg_similarity = signals.get("avg_similarity", 0)
    avg_success_score = signals.get("avg_success_score", 0)
    dominant_industry = signals.get("dominant_industry", "Unknown")

    assessment_parts = []

    if overall_score >= 75:
        assessment_parts.append(
            "This idea shows strong evidence-backed potential compared with similar startups in the dataset."
        )
    elif overall_score >= 55:
        assessment_parts.append(
            "This idea appears moderately promising, but the evidence suggests it still needs sharper validation."
        )
    else:
        assessment_parts.append(
            "This idea currently looks risky based on available peer patterns in the dataset."
        )

    if avg_similarity >= 0.35:
        assessment_parts.append(
            "The retrieval quality is reasonably strong, so the system has a meaningful basis for comparison."
        )
    elif avg_similarity >= 0.20:
        assessment_parts.append(
            "The retrieved startups are somewhat relevant, though the evidence is not extremely strong."
        )
    else:
        assessment_parts.append(
            "The system found only weakly similar peer cases, so conclusions should be treated cautiously."
        )

    if success_ratio > failure_ratio:
        assessment_parts.append(
            "Among retrieved peers, successful outcomes appear more common than failed ones."
        )
    elif failure_ratio > success_ratio:
        assessment_parts.append(
            "Among retrieved peers, failed outcomes appear more common than successful ones."
        )
    else:
        assessment_parts.append(
            "Peer outcomes are mixed, without a dominant success pattern."
        )

    why_it_may_work = (
        f"The idea aligns most closely with the {dominant_industry} peer group, "
        f"where the average peer success score is {avg_success_score} and the peer success ratio is {success_ratio}. "
        f"If execution quality is above average, the concept may still earn meaningful traction."
    )


    risk_lines = []
    for flag in risk.get("risk_flags", []):
        risk_lines.append(f"- {flag}")
    if not risk_lines:
        risk_lines.append("- No major rule-based risk flags were triggered, but uncertainty remains.")

    scenario_text = "\n\n".join(
        [
            f"**Scenario Confidence:** {scenarios.get('confidence', 'Unknown')}",
            scenarios.get("summary", ""),
            _format_scenario_block("Best Case", scenarios.get("best_case", {})),
            _format_scenario_block("Base Case", scenarios.get("base_case", {})),
            _format_scenario_block("Worst Case", scenarios.get("worst_case", {})),
        ]
    )
    recommendation_lines = [f"- {item}" for item in recommendations] if recommendations else ["- No recommendation generated."]

    similar_text = _top_similar_summary(similar_startups, top_n=3)

    return f"""
## Overall Assessment
Score: **{overall_score} / 100**  
Verdict: **{verdict}**  
Risk Level: **{risk_level}**

{' '.join(assessment_parts)}

## Why This Idea May Work
{why_it_may_work}

## Main Risks
{chr(10).join(risk_lines)}

## What Similar Startups Suggest
{similar_text}

## Future Scenarios
{scenario_text}

## Recommended Next Steps
{chr(10).join(recommendation_lines)}
""".strip()


def generate_final_report(
    user_idea: str,
    rag_context: Dict[str, Any],
    scoring: Dict[str, Any],
    risk: Dict[str, Any],
    scenarios: Dict[str, str],
    recommendations: List[str],
) -> Dict[str, Any]:
    similar_startups = rag_context.get("similar_startups", [])
    signals = rag_context.get("aggregated_signals", {})

    structured_summary = {
        "overall_score": scoring.get("overall_score"),
        "verdict": scoring.get("verdict"),
        "risk_level": risk.get("risk_level"),
        "avg_peer_success_score": signals.get("avg_success_score"),
        "peer_success_ratio": signals.get("success_ratio"),
        "peer_failure_ratio": signals.get("failure_ratio"),
        "avg_similarity": signals.get("avg_similarity"),
        "max_similarity": signals.get("max_similarity"),
        "avg_funding": signals.get("avg_funding"),
        "dominant_industry": signals.get("dominant_industry"),
        "top_similar_startups": similar_startups[:5],
    }

    narrative_summary = _build_narrative_summary(
        user_idea=user_idea,
        rag_context=rag_context,
        scoring=scoring,
        risk=risk,
        scenarios=scenarios,
        recommendations=recommendations,
    )

    return {
        "idea": user_idea,
        "structured_summary": structured_summary,
        "narrative_summary": narrative_summary,
        "evidence_text": rag_context.get("evidence_text", ""),
    }
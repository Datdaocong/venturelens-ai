from __future__ import annotations


def generate_report(
    structured_idea: dict,
    scoring: dict,
    scenarios: dict,
    risks: dict,
    recommendations: dict,
    similar_startups: list,
    retrieval_summary: dict | None = None,
) -> str:
    retrieval_summary = retrieval_summary or {}

    lines = []
    lines.append("# VentureLens Analysis Report")
    lines.append("")

    lines.append("## 1. Structured Idea")
    for key, value in structured_idea.items():
        lines.append(f"- **{key}**: {value}")
    lines.append("")

    lines.append("## 2. Score Summary")
    lines.append(f"- **Overall Score**: {scoring.get('overall_score', 'N/A')}")
    for k, v in scoring.get("scores", {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.append(f"- **Interpretation**: {scoring.get('summary', '')}")
    lines.append("")

    lines.append("## 3. Evidence From Similar Startups")
    if retrieval_summary:
        lines.append(f"- **Peer count**: {retrieval_summary.get('peer_count', 0)}")
        lines.append(f"- **Average similarity**: {retrieval_summary.get('avg_similarity', 0)}")
        lines.append(f"- **Average success score**: {retrieval_summary.get('avg_success_score', 0)}")
        lines.append(f"- **Average funding rounds**: {retrieval_summary.get('avg_funding_round_count', 0)}")
        lines.append(f"- **Average funding (USD)**: {retrieval_summary.get('avg_total_funding_usd', 0)}")
        lines.append(f"- **Acquisition rate**: {retrieval_summary.get('acquisition_rate', 0)}")
        lines.append(f"- **IPO rate**: {retrieval_summary.get('ipo_rate', 0)}")
        lines.append(f"- **Common outcomes**: {', '.join(retrieval_summary.get('top_outcomes', []))}")
        lines.append(f"- **Common industries**: {', '.join(retrieval_summary.get('top_industries', []))}")
        lines.append("")

    if similar_startups:
        for s in similar_startups[:5]:
            lines.append(
                f"- **{s.get('name', 'Unknown')}** | "
                f"industry={s.get('industry', '')} | "
                f"outcome={s.get('outcome_label', '')} | "
                f"funding_rounds={s.get('funding_round_count', 0)} | "
                f"success_score={s.get('success_score', 0)} | "
                f"similarity={round(float(s.get('similarity', 0)), 3)}"
            )
    else:
        lines.append("- No comparable startups found.")
    lines.append("")

    lines.append("## 4. Risk Analysis")
    for risk in risks.get("top_risks", []):
        lines.append(f"- {risk}")
    lines.append(f"- **Risk level**: {risks.get('risk_level', 'unknown')}")
    for e in risks.get("evidence", []):
        lines.append(f"- Evidence: {e}")
    lines.append("")

    lines.append("## 5. Future Scenarios")
    lines.append(f"- **Optimistic**: {scenarios.get('optimistic', '')}")
    lines.append(f"- **Realistic**: {scenarios.get('realistic', '')}")
    lines.append(f"- **Risky**: {scenarios.get('risky', '')}")
    lines.append("")

    lines.append("## 6. Recommendations")
    lines.append(f"- **Verdict**: {recommendations.get('verdict', '')}")
    for step in recommendations.get("next_steps", []):
        lines.append(f"- {step}")
    lines.append(f"- **MVP focus**: {recommendations.get('mvp_focus', '')}")
    lines.append(f"- **Validation focus**: {recommendations.get('validation_focus', '')}")
    lines.append(f"- **Strategic note**: {recommendations.get('strategic_note', '')}")

    return "\n".join(lines)
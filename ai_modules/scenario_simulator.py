from __future__ import annotations

from typing import Any, Dict, List


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _build_best_case(
    user_idea: str,
    overall_score: float,
    success_ratio: float,
    avg_similarity: float,
    dominant_industry: str,
    risk_level: str,
) -> Dict[str, Any]:
    if overall_score >= 75 and risk_level == "Low":
        title = "High-traction breakout"
        description = (
            f"The idea gains strong early traction in the {dominant_industry} space, "
            "finds a clear customer pain point, and converts early interest into repeat usage."
        )
        why = (
            "Retrieved peers suggest that similar startup patterns can succeed when the positioning is clear, "
            "the problem is urgent, and execution quality is above average."
        )
        trigger = "Strong early validation from a narrowly defined user segment."
        warning_signs = [
            "Users like the concept but do not return",
            "Interest exists but conversion remains weak",
            "The product message is exciting but too broad",
        ]
        strategic_action = (
            "Double down on the strongest niche, measure retention aggressively, "
            "and turn early traction into a repeatable go-to-market engine."
        )
    else:
        title = "Selective traction upside"
        description = (
            "The idea can still achieve meaningful traction, but only after narrowing the product scope, "
            "clarifying the value proposition, and focusing on one user group."
        )
        why = (
            "Even when overall signals are mixed, some startup ideas improve significantly after sharper positioning "
            "and better validation discipline."
        )
        trigger = "A clear wedge use case that solves one painful problem very well."
        warning_signs = [
            "Feature list keeps growing without stronger validation",
            "Too many audiences are targeted at once",
            "Users say the idea is interesting but not urgent",
        ]
        strategic_action = (
            "Cut the MVP to one high-value workflow, validate it deeply, "
            "and avoid scaling before a convincing usage pattern appears."
        )

    return {
        "title": title,
        "description": description,
        "why_this_could_happen": why,
        "key_trigger": trigger,
        "warning_signs": warning_signs,
        "strategic_action": strategic_action,
    }


def _build_base_case(
    overall_score: float,
    success_ratio: float,
    failure_ratio: float,
    avg_similarity: float,
    risk_level: str,
) -> Dict[str, Any]:
    if success_ratio >= 0.50 and avg_similarity >= 0.25:
        title = "Moderate traction with execution pressure"
        description = (
            "The startup reaches early validation and some user traction, "
            "but growth depends heavily on execution quality, retention, and focus."
        )
        why = (
            "The peer group contains enough relevant examples to suggest the idea is plausible, "
            "but not enough to assume strong breakout performance by default."
        )
        trigger = "Consistent user feedback that confirms a repeatable problem-solution fit."
        warning_signs = [
            "Users try the product once but do not build habits",
            "Acquisition works better than retention",
            "The team is shipping features faster than learning from users",
        ]
        strategic_action = (
            "Track retention, activation, and user pain-point clarity before pushing for scale."
        )
    elif failure_ratio > success_ratio:
        title = "Slow progress in a difficult segment"
        description = (
            "The startup struggles to separate itself from weaker peer patterns and may show slow adoption."
        )
        why = (
            "Retrieved peers suggest this category has meaningful failure risk, "
            "especially when differentiation and timing are weak."
        )
        trigger = "A stronger product angle or clearer distribution channel than similar failed peers."
        warning_signs = [
            "Early users do not clearly explain why this is better",
            "Market response is polite but not enthusiastic",
            "The startup competes on features alone",
        ]
        strategic_action = (
            "Reposition the idea, sharpen differentiation, and test whether the pain point is truly urgent."
        )
    else:
        title = "Plausible but unproven path"
        description = (
            "The startup has some promising signs, but evidence remains mixed and commercial success is uncertain."
        )
        why = (
            "The system found partial support from peer startups, but not enough to treat the opportunity as clearly de-risked."
        )
        trigger = "Evidence that users repeatedly return, pay, or refer others."
        warning_signs = [
            "Validation relies on compliments rather than behavior",
            "Customers understand the product but do not prioritize it",
            "The startup message sounds useful but not must-have",
        ]
        strategic_action = (
            "Use milestone-based validation and avoid overcommitting resources before stronger proof appears."
        )

    return {
        "title": title,
        "description": description,
        "why_this_could_happen": why,
        "key_trigger": trigger,
        "warning_signs": warning_signs,
        "strategic_action": strategic_action,
    }


def _build_worst_case(
    overall_score: float,
    avg_similarity: float,
    failure_ratio: float,
    risk_level: str,
) -> Dict[str, Any]:
    if risk_level == "High":
        title = "Early shutdown risk"
        description = (
            "The startup fails to achieve convincing validation, struggles to retain users, "
            "and may shut down early after weak traction."
        )
        why = (
            "The evidence suggests a combination of weak retrieval fit, poor peer outcomes, "
            "or limited support from comparable startups."
        )
        trigger = "No repeat usage or no convincing problem-solution fit after initial testing."
        warning_signs = [
            "User interviews sound positive but behavior stays weak",
            "No meaningful retention after launch",
            "The team keeps changing direction without better evidence",
        ]
        strategic_action = (
            "Reduce burn, narrow the problem, and test one focused use case before continuing broader development."
        )
    elif avg_similarity < 0.20:
        title = "Unclear market fit"
        description = (
            "The startup enters a vague or poorly defined category where historical peer evidence is weak."
        )
        why = (
            "The idea may be too broad, too novel for the current dataset, or described in a way that does not align "
            "with known successful patterns."
        )
        trigger = "A much clearer articulation of the target user, problem, and workflow."
        warning_signs = [
            "The idea sounds impressive but difficult to explain simply",
            "Potential users do not immediately recognize the pain point",
            "The product keeps shifting categories",
        ]
        strategic_action = (
            "Rewrite the value proposition in a simpler, narrower way and retest with real users."
        )
    else:
        title = "Weak monetization and low retention"
        description = (
            "The startup gets some initial interest but cannot sustain engagement or convert usage into a business."
        )
        why = (
            "Some ideas generate curiosity without solving a painful enough problem to create strong retention or willingness to pay."
        )
        trigger = "Proof that users come back consistently and treat the product as part of a real workflow."
        warning_signs = [
            "Users say they like it, but do not depend on it",
            "Growth is driven by curiosity rather than need",
            "Revenue logic remains unclear after MVP testing",
        ]
        strategic_action = (
            "Focus on retention and value capture before adding complexity or chasing top-line growth."
        )

    return {
        "title": title,
        "description": description,
        "why_this_could_happen": why,
        "key_trigger": trigger,
        "warning_signs": warning_signs,
        "strategic_action": strategic_action,
    }


def simulate_scenarios(
    user_idea: str,
    scoring: Dict[str, Any],
    risk: Dict[str, Any],
    peer_signals: Dict[str, Any],
) -> Dict[str, Any]:
    overall_score = float(scoring.get("overall_score", 0))
    success_ratio = float(peer_signals.get("success_ratio", 0))
    failure_ratio = float(peer_signals.get("failure_ratio", 0))
    avg_similarity = float(peer_signals.get("avg_similarity", 0))
    dominant_industry = str(peer_signals.get("dominant_industry", "Unknown"))
    risk_level = str(risk.get("risk_level", "Medium"))

    best_case = _build_best_case(
        user_idea=user_idea,
        overall_score=overall_score,
        success_ratio=success_ratio,
        avg_similarity=avg_similarity,
        dominant_industry=dominant_industry,
        risk_level=risk_level,
    )

    base_case = _build_base_case(
        overall_score=overall_score,
        success_ratio=success_ratio,
        failure_ratio=failure_ratio,
        avg_similarity=avg_similarity,
        risk_level=risk_level,
    )

    worst_case = _build_worst_case(
        overall_score=overall_score,
        avg_similarity=avg_similarity,
        failure_ratio=failure_ratio,
        risk_level=risk_level,
    )

    confidence = "High"
    if avg_similarity < 0.30 or risk_level == "Medium":
        confidence = "Medium"
    if avg_similarity < 0.18 or risk_level == "High":
        confidence = "Low"

    scenario_summary = (
        "The future outlook is shaped mainly by retrieval strength, peer outcome quality, "
        "and whether the idea can achieve narrow, behavior-based validation early."
    )

    return {
        "confidence": confidence,
        "summary": scenario_summary,
        "best_case": best_case,
        "base_case": base_case,
        "worst_case": worst_case,
    }
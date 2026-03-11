import streamlit as st
from ai_modules.idea_structurer import structure_startup_idea
from ai_modules.scoring_engine import score_startup
from ai_modules.scenario_simulator import simulate_future_scenarios
from ai_modules.risk_analyzer import analyze_risks
from ai_modules.recommendation_engine import generate_recommendations
from ai_modules.report_generator import generate_report

st.set_page_config(page_title="VentureLens AI", page_icon="🚀", layout="wide")

st.title("🚀 VentureLens AI")
st.subheader("AI Startup Idea Analyzer and Scenario Simulator")

startup_idea = st.text_area(
    "Describe your startup idea:",
    placeholder="Example: An AI platform that helps students automatically summarize lecture recordings and generate quizzes...",
    height=180
)

show_details = st.checkbox("Show technical analysis details")


if "startup_idea" not in st.session_state:
    st.session_state.startup_idea = ""

if st.button("Use Sample Idea"):
    st.session_state.startup_idea = (
        "An AI platform that helps students summarize lecture recordings, "
        "generate quizzes, and create personalized study plans for exams."
    )

startup_idea = st.text_area(
    "Describe your startup idea:",
    value=st.session_state.startup_idea,
    placeholder="Example: An AI platform that helps students automatically summarize lecture recordings and generate quizzes...",
    height=180
)

if st.button("Analyze Idea"):
    if startup_idea.strip():
        with st.spinner("Preparing your founder briefing..."):
            structured_idea = structure_startup_idea(startup_idea)
            scoring = score_startup(structured_idea)
            scenarios = simulate_future_scenarios(structured_idea, scoring)
            risks = analyze_risks(structured_idea, scoring, scenarios)
            recommendations = generate_recommendations(
                structured_idea,
                scoring,
                scenarios,
                risks
            )
            report = generate_report(
                structured_idea,
                scoring,
                scenarios,
                risks,
                recommendations
            )

        st.success("Founder briefing ready.")

        # =========================
        # SCORE OVERVIEW
        # =========================
        st.write("## Startup Snapshot")

        overall_score = scoring.get("overall_score", 0)
        summary = scoring.get("summary", "No summary available.")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Overall Score", f"{overall_score}/10")

        with col2:
            st.info(summary)

        # =========================
        # SCORE BREAKDOWN
        # =========================
        st.write("## Score Breakdown")

        score_map = scoring.get("scores", {})

        if score_map:
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Problem Severity", score_map.get("problem_severity", "N/A"))
                st.metric("Market Size", score_map.get("market_size", "N/A"))

            with c2:
                st.metric("Competition", score_map.get("competition", "N/A"))
                st.metric("Differentiation", score_map.get("differentiation", "N/A"))

            with c3:
                st.metric("Monetization", score_map.get("monetization", "N/A"))
                st.metric("Feasibility", score_map.get("feasibility", "N/A"))

            with c4:
                st.metric("Distribution", score_map.get("distribution", "N/A"))
                st.metric("Speed to MVP", score_map.get("speed_to_mvp", "N/A"))
        else:
            st.warning("Score breakdown not available.")

        # =========================
        # FUTURE SCENARIOS
        # =========================
        st.write("## Future Scenarios")

        sc1, sc2, sc3 = st.columns(3)

        with sc1:
            st.markdown("### Best-Case")
            st.success(scenarios.get("best_case", "Not available."))

        with sc2:
            st.markdown("### Realistic")
            st.info(scenarios.get("realistic_case", "Not available."))

        with sc3:
            st.markdown("### Worst-Case")
            st.error(scenarios.get("worst_case", "Not available."))

        triggers = scenarios.get("key_triggers", [])
        if triggers:
            st.write("### Key Triggers")
            for trigger in triggers:
                st.write(f"- {trigger}")

        # =========================
        # RISKS + RECOMMENDATIONS
        # =========================
        left_col, right_col = st.columns(2)

        with left_col:
            st.write("## Key Risks")

            top_risks = risks.get("top_risks", [])
            dangerous_assumptions = risks.get("dangerous_assumptions", [])
            risk_summary = risks.get("risk_summary", "")

            if risk_summary:
                st.warning(risk_summary)

            st.markdown("### Top Risks")
            for risk in top_risks:
                st.write(f"- {risk}")

            st.markdown("### Dangerous Assumptions")
            for assumption in dangerous_assumptions:
                st.write(f"- {assumption}")

        with right_col:
            st.write("## Strategic Recommendations")

            next_steps = recommendations.get("next_steps", [])
            mvp_suggestion = recommendations.get("mvp_suggestion", "")
            validation_focus = recommendations.get("validation_focus", "")

            st.markdown("### Next Steps")
            for i, step in enumerate(next_steps, start=1):
                st.write(f"{i}. {step}")

            st.markdown("### MVP Suggestion")
            st.success(mvp_suggestion if mvp_suggestion else "Not available.")

            st.markdown("### Validation Focus")
            st.info(validation_focus if validation_focus else "Not available.")

        # =========================
        # FOUNDER BRIEFING REPORT
        # =========================
        st.write("## Founder Briefing")
        st.markdown(report)

        # =========================
        # TECHNICAL DETAILS
        # =========================
        if show_details:
            st.divider()
            st.write("## Technical Analysis Details")

            with st.expander("Structured Startup Idea"):
                st.json(structured_idea)

            with st.expander("Startup Score JSON"):
                st.json(scoring)

            with st.expander("Future Scenarios JSON"):
                st.json(scenarios)

            with st.expander("Risk Analysis JSON"):
                st.json(risks)

            with st.expander("Recommendations JSON"):
                st.json(recommendations)

    else:
        st.warning("Please enter a startup idea first.")
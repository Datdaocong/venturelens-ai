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
        st.markdown(report)

        if show_details:
            st.divider()

            st.write("## Technical Analysis Details")

            st.write("### Structured Startup Idea")
            st.json(structured_idea)

            st.write("### Startup Score")
            st.json(scoring)

            st.write("### Future Scenarios")
            st.json(scenarios)

            st.write("### Key Risks")
            st.json(risks)

            st.write("### Recommendations")
            st.json(recommendations)
    else:
        st.warning("Please enter a startup idea first.")
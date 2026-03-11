import streamlit as st
from ai_modules.full_analysis import generate_full_analysis
from ai_modules.report_generator import generate_report

st.set_page_config(
    page_title="VentureLens",
    layout="wide"
)

st.title("VentureLens")
st.caption("Startup idea analysis and strategic scenario assessment")

# ---------------------------
# SESSION STATE
# ---------------------------
if "startup_idea" not in st.session_state:
    st.session_state.startup_idea = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "report" not in st.session_state:
    st.session_state.report = None

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.subheader("Analysis Settings")

    analysis_mode = st.radio(
        "Mode",
        ["Founder", "Investor", "Brutal"],
        index=0,
        key="analysis_mode"
    )

    show_details = st.checkbox(
        "Show technical details",
        value=False,
        key="show_details"
    )

    st.divider()

    if st.button("Use Sample Idea", use_container_width=True):
        st.session_state.startup_idea = (
            "An AI platform that helps university students summarize lecture recordings, "
            "generate quizzes, and create personalized study plans for exams."
        )

    if st.button("Clear", use_container_width=True):
        st.session_state.startup_idea = ""
        st.session_state.analysis = None
        st.session_state.report = None

# ---------------------------
# MAIN INPUT
# ---------------------------
startup_idea = st.text_area(
    "Startup idea",
    value=st.session_state.startup_idea,
    height=180,
    placeholder="Describe the startup idea, target user, and what problem it solves.",
    key="startup_input"
)

col_a, col_b = st.columns([1, 1])

with col_a:
    analyze_clicked = st.button("Run Analysis", use_container_width=True, key="run_analysis")

with col_b:
    report_clicked = st.button("Generate Briefing Memo", use_container_width=True, key="generate_report")

# ---------------------------
# ANALYSIS
# ---------------------------
if analyze_clicked:
    if startup_idea.strip():
        with st.spinner("Running strategic analysis..."):
            analysis = generate_full_analysis(startup_idea, analysis_mode)
            st.session_state.analysis = analysis
            st.session_state.report = None
        st.success("Analysis complete.")
    else:
        st.warning("Enter a startup idea before running analysis.")

analysis = st.session_state.analysis

# ---------------------------
# DISPLAY ANALYSIS
# ---------------------------
if analysis:
    structured_idea = analysis.get("structured_idea", {})
    scoring = analysis.get("scoring", {})
    scenarios = analysis.get("scenarios", {})
    risks = analysis.get("risks", {})
    recommendations = analysis.get("recommendations", {})

    overall_score = scoring.get("overall_score", 0)
    score_map = scoring.get("scores", {})
    score_summary = scoring.get("summary", "No summary available.")

    st.divider()
    st.subheader("Startup Snapshot")

    snap_1, snap_2, snap_3 = st.columns([1, 1, 2])

    with snap_1:
        st.metric("Overall Score", f"{overall_score}/10")

    with snap_2:
        st.metric("Mode", analysis_mode)

    with snap_3:
        st.info(score_summary)

    st.subheader("Score Breakdown")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Problem Severity", score_map.get("problem_severity", "N/A"))
        st.metric("Market Size", score_map.get("market_size", "N/A"))

    with m2:
        st.metric("Competition", score_map.get("competition", "N/A"))
        st.metric("Differentiation", score_map.get("differentiation", "N/A"))

    with m3:
        st.metric("Monetization", score_map.get("monetization", "N/A"))
        st.metric("Feasibility", score_map.get("feasibility", "N/A"))

    with m4:
        st.metric("Distribution", score_map.get("distribution", "N/A"))
        st.metric("Speed to MVP", score_map.get("speed_to_mvp", "N/A"))

    st.subheader("Future Outlook")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("**Best-Case**")
        st.success(scenarios.get("best_case", "Not available."))

    with f2:
        st.markdown("**Realistic Case**")
        st.info(scenarios.get("realistic_case", "Not available."))

    with f3:
        st.markdown("**Worst-Case**")
        st.error(scenarios.get("worst_case", "Not available."))

    triggers = scenarios.get("key_triggers", [])
    if triggers:
        st.markdown("**Key Triggers**")
        for trigger in triggers:
            st.write(f"- {trigger}")

    left, right = st.columns(2)

    with left:
        st.subheader("Core Risks")

        risk_summary = risks.get("risk_summary", "")
        if risk_summary:
            st.warning(risk_summary)

        st.markdown("**Top Risks**")
        for item in risks.get("top_risks", []):
            st.write(f"- {item}")

        st.markdown("**Dangerous Assumptions**")
        for item in risks.get("dangerous_assumptions", []):
            st.write(f"- {item}")

    with right:
        st.subheader("Recommended Actions")

        st.markdown("**Next Steps**")
        for i, step in enumerate(recommendations.get("next_steps", []), start=1):
            st.write(f"{i}. {step}")

        st.markdown("**MVP Suggestion**")
        st.success(recommendations.get("mvp_suggestion", "Not available."))

        st.markdown("**Validation Focus**")
        st.info(recommendations.get("validation_focus", "Not available."))

    # ---------------------------
    # REPORT BUTTON ACTION
    # ---------------------------
    if report_clicked:
        with st.spinner("Writing briefing memo..."):
            report = generate_report(
                structured_idea,
                scoring,
                scenarios,
                risks,
                recommendations,
                analysis_mode
            )
            st.session_state.report = report

# ---------------------------
# REPORT
# ---------------------------
if st.session_state.report:
    st.divider()
    st.subheader("Briefing Memo")
    st.markdown(st.session_state.report)

# ---------------------------
# TECHNICAL DETAILS
# ---------------------------
if analysis and show_details:
    st.divider()
    st.subheader("Technical Details")

    with st.expander("Structured Idea"):
        st.json(analysis.get("structured_idea", {}))

    with st.expander("Scoring"):
        st.json(analysis.get("scoring", {}))

    with st.expander("Scenarios"):
        st.json(analysis.get("scenarios", {}))

    with st.expander("Risks"):
        st.json(analysis.get("risks", {}))

    with st.expander("Recommendations"):
        st.json(analysis.get("recommendations", {}))
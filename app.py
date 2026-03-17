from __future__ import annotations

import streamlit as st
import pandas as pd

from ai_modules.full_analysis import run_full_analysis
from ai_modules.radar_chart import create_radar_figure


st.set_page_config(
    page_title="VentureLens AI",
    page_icon="🚀",
    layout="wide",
)


def render_header() -> None:
    st.title("🚀 VentureLens AI")
    st.caption(
        "Analyze startup ideas using real-world startup data, retrieval, scoring, risk signals, and grounded recommendations."
    )


def render_intro() -> None:
    with st.expander("How VentureLens works", expanded=False):
        st.markdown(
            """
**Pipeline**
1. Retrieve similar startups from the dataset  
2. Build evidence-backed peer signals  
3. Score the idea using data-driven metrics  
4. Analyze risk and future scenarios  
5. Generate grounded recommendations and summary
"""
        )


def render_score_cards(result: dict) -> None:
    scoring = result["scoring"]
    risk = result["risk"]
    signals = result["aggregated_signals"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Overall Score", f'{scoring.get("overall_score", 0):.2f}')

    with col2:
        st.metric("Verdict", scoring.get("verdict", "Unknown"))

    with col3:
        st.metric("Risk Level", risk.get("risk_level", "Unknown"))

    with col4:
        st.metric("Peers Retrieved", signals.get("num_peers", 0))


def render_radar_and_signals(result: dict) -> None:
    scoring = result["scoring"]
    risk = result["risk"]
    signals = result["aggregated_signals"]

    left_col, right_col = st.columns([1.25, 1])

    with left_col:
        st.subheader("Startup Radar")
        radar_fig = create_radar_figure(scoring=scoring, risk=risk)
        st.plotly_chart(radar_fig, use_container_width=True)

    with right_col:
        st.subheader("Peer Signals")

        peer_df = pd.DataFrame(
            [
                {"Metric": "Dominant Industry", "Value": signals.get("dominant_industry", "Unknown")},
                {"Metric": "Average Peer Success Score", "Value": signals.get("avg_success_score", 0)},
                {"Metric": "Average Similarity", "Value": signals.get("avg_similarity", 0)},
                {"Metric": "Max Similarity", "Value": signals.get("max_similarity", 0)},
                {"Metric": "Success Ratio", "Value": signals.get("success_ratio", 0)},
                {"Metric": "Failure Ratio", "Value": signals.get("failure_ratio", 0)},
                {"Metric": "Average Funding (USD)", "Value": signals.get("avg_funding", 0)},
            ]
        )
        st.dataframe(peer_df, use_container_width=True, hide_index=True)

        st.subheader("Risk Flags")
        risk_flags = risk.get("risk_flags", [])
        if risk_flags:
            for flag in risk_flags:
                st.write(f"- {flag}")
        else:
            st.write("No major rule-based risk flags detected.")


def render_similar_startups(result: dict) -> None:
    st.subheader("Similar Startups Retrieved")

    similar_startups = result.get("similar_startups", [])
    if not similar_startups:
        st.info("No similar startups found in the dataset.")
        return

    df_similar = pd.DataFrame(similar_startups).copy()

    preferred_order = [
        "name",
        "industry",
        "funding",
        "success_score",
        "outcome_label",
        "similarity_score",
        "description",
    ]
    cols = [c for c in preferred_order if c in df_similar.columns]
    df_similar = df_similar[cols]

    st.dataframe(df_similar, use_container_width=True, hide_index=True)


def render_summary_and_scenarios(result: dict) -> None:
    report = result["report"]
    scenarios = result["scenarios"]

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Narrative Summary")
        st.markdown(report.get("narrative_summary", "No summary generated."))

    with col2:
        st.subheader("Future Scenarios")
        st.caption(f"Scenario confidence: {scenarios.get('confidence', 'Unknown')}")
        st.write(scenarios.get("summary", ""))

        for label, key in [
            ("Best Case", "best_case"),
            ("Base Case", "base_case"),
            ("Worst Case", "worst_case"),
        ]:
            scenario = scenarios.get(key, {})

            with st.expander(
                f"{label}: {scenario.get('title', 'N/A')}",
                expanded=(key == "base_case"),
            ):
                st.markdown(f"**Description**  \n{scenario.get('description', 'N/A')}")
                st.markdown(
                    f"**Why this could happen**  \n{scenario.get('why_this_could_happen', 'N/A')}"
                )
                st.markdown(f"**Key trigger**  \n{scenario.get('key_trigger', 'N/A')}")

                st.markdown("**Warning signs**")
                warning_signs = scenario.get("warning_signs", [])
                if warning_signs:
                    for item in warning_signs:
                        st.write(f"- {item}")
                else:
                    st.write("- None")

                st.markdown(
                    f"**Strategic action**  \n{scenario.get('strategic_action', 'N/A')}"
                )


def render_recommendations(result: dict) -> None:
    recommendations = result.get("recommendations", [])

    st.subheader("Recommended Next Steps")
    if recommendations:
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.write("No recommendations generated.")


def render_evidence(result: dict) -> None:
    report = result["report"]

    with st.expander("View Retrieval Evidence", expanded=False):
        st.text(report.get("evidence_text", "No evidence available."))


def render_footer() -> None:
    st.markdown("---")
    st.caption(
        "VentureLens AI uses dataset-grounded retrieval and scoring. Narrative output is based on peer evidence rather than pure LLM guessing."
    )


def main() -> None:
    render_header()
    render_intro()

    default_idea = (
        "An AI platform that helps university students detect academic integrity risks, "
        "improve writing originality, and receive structured feedback before submission."
    )

    user_idea = st.text_area(
        "Enter your startup idea",
        value=default_idea,
        height=180,
        placeholder="Describe your startup idea, product, target user, and problem you want to solve...",
    )

    top_k = st.slider("Number of similar startups to retrieve", min_value=3, max_value=10, value=5)

    analyze_clicked = st.button("Analyze Startup Idea", type="primary", use_container_width=True)

    if analyze_clicked:
        if not user_idea.strip():
            st.warning("Please enter a startup idea first.")
            st.stop()

        with st.spinner("Analyzing with VentureLens AI..."):
            try:
                result = run_full_analysis(user_idea=user_idea, top_k=top_k)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        render_score_cards(result)
        st.markdown("---")

        render_radar_and_signals(result)
        st.markdown("---")

        render_similar_startups(result)
        st.markdown("---")

        render_summary_and_scenarios(result)
        st.markdown("---")

        render_recommendations(result)
        render_evidence(result)

    render_footer()


if __name__ == "__main__":
    main()
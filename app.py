import streamlit as st
import pandas as pd

from ai_modules.full_analysis import run_full_analysis

st.set_page_config(page_title="VentureLens AI", page_icon="🚀", layout="wide")

st.title("🚀 VentureLens AI")
st.caption("AI startup idea analysis grounded in real startup dataset evidence")

idea = st.text_area(
    "Describe your startup idea",
    height=180,
    placeholder="Example: An AI copilot that helps startup founders prepare investor updates, fundraising narratives, and KPI summaries."
)

if st.button("Analyze"):
    if not idea.strip():
        st.warning("Please enter a startup idea first.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                result = run_full_analysis(idea)

                tabs = st.tabs([
                    "Structured Idea",
                    "Similar Startups",
                    "Scoring",
                    "Risks & Scenarios",
                    "Recommendations",
                    "Report",
                ])

                with tabs[0]:
                    st.json(result["structured_idea"])

                with tabs[1]:
                    similar = result.get("similar_startups", [])
                    retrieval_summary = result.get("retrieval_summary", {})

                    st.subheader("Retrieval Summary")
                    st.json(retrieval_summary)

                    if similar:
                        df = pd.DataFrame(similar)
                        preferred_cols = [
                            "name",
                            "industry",
                            "hq_country",
                            "funding_round_count",
                            "total_funding_usd",
                            "success_score",
                            "outcome_label",
                            "similarity",
                        ]
                        existing_cols = [c for c in preferred_cols if c in df.columns]
                        st.dataframe(df[existing_cols] if existing_cols else df, use_container_width=True)
                    else:
                        st.info("No similar startups found.")

                with tabs[2]:
                    st.json(result["scoring"])

                with tabs[3]:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Risks")
                        st.json(result["risks"])
                    with col2:
                        st.subheader("Scenarios")
                        st.json(result["scenarios"])

                with tabs[4]:
                    st.json(result["recommendations"])

                with tabs[5]:
                    st.markdown(result["report"])

            except Exception as e:
                st.error(f"Error while analyzing idea: {e}")
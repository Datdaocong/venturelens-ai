import streamlit as st
import pandas as pd

from ai_modules.full_analysis import run_full_analysis
from ai_modules.data_loader import load_ai_dataset
from ai_modules.similarity_bridge import retrieve_similar_startups


st.set_page_config(
    page_title="VentureLens AI",
    page_icon="🚀",
    layout="wide",
)


@st.cache_resource
def warm_up_system():
    load_ai_dataset()
    retrieve_similar_startups("AI startup", top_k=3)
    return True


def pretty_score_name(key: str) -> str:
    mapping = {
        "market_attractiveness": "Market Attractiveness",
        "feasibility": "Feasibility",
        "competitive_pressure": "Competitive Pressure",
        "signal_strength": "Data Signal Strength",
    }
    return mapping.get(key, key.replace("_", " ").title())


def pretty_summary_name(key: str) -> str:
    mapping = {
        "peer_count": "Peer Startups",
        "avg_similarity": "Avg Similarity",
        "avg_success_score": "Avg Success Score",
        "avg_funding_round_count": "Avg Funding Rounds",
        "avg_total_funding_usd": "Avg Funding (USD)",
        "acquisition_rate": "Acquisition Rate",
        "ipo_rate": "IPO Rate",
        "top_outcomes": "Common Outcomes",
        "top_industries": "Top Industries",
    }
    return mapping.get(key, key.replace("_", " ").title())


def pretty_outcome(value: str) -> str:
    mapping = {
        "ipo": "IPO",
        "acquired": "Acquired",
        "closed": "Closed",
        "funded_growth": "Funded Growth",
        "early_or_unknown": "Early / Unknown",
        "unknown": "Unknown",
    }
    return mapping.get(str(value).strip().lower(), value)


def render_kv_block(data: dict):
    if not data:
        st.info("No data available.")
        return

    for key, value in data.items():
        label = key.replace("_", " ").title()
        if isinstance(value, list):
            st.markdown(f"**{label}:**")
            for item in value:
                st.markdown(f"- {item}")
        else:
            st.markdown(f"**{label}:** {value}")


def render_similar_startups(similar_startups: list, retrieval_summary: dict):
    st.subheader("Market Evidence")

    if retrieval_summary:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Peers", retrieval_summary.get("peer_count", 0))
        c2.metric("Similarity", retrieval_summary.get("avg_similarity", 0))
        c3.metric("Success Score", retrieval_summary.get("avg_success_score", 0))
        c4.metric("Funding Rounds", retrieval_summary.get("avg_funding_round_count", 0))

        rows = []
        for k, v in retrieval_summary.items():
            if k in {"peer_count", "avg_similarity", "avg_success_score", "avg_funding_round_count"}:
                continue
            if isinstance(v, list):
                v = ", ".join(map(str, v)) if v else "N/A"
            rows.append({"Metric": pretty_summary_name(k), "Value": v})

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Top Similar Startups")

    if not similar_startups:
        st.info("No similar startups found.")
        return

    df = pd.DataFrame(similar_startups)
    cols = [
        "name",
        "industry",
        "hq_country",
        "funding_round_count",
        "total_funding_usd",
        "success_score",
        "outcome_label",
        "similarity",
    ]
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    if "outcome_label" in df.columns:
        df["outcome_label"] = df["outcome_label"].apply(pretty_outcome)

    df = df.rename(columns={
        "name": "Startup",
        "industry": "Industry",
        "hq_country": "Country",
        "funding_round_count": "Funding Rounds",
        "total_funding_usd": "Total Funding (USD)",
        "success_score": "Success Score",
        "outcome_label": "Outcome",
        "similarity": "Similarity",
    })

    st.dataframe(df, use_container_width=True, hide_index=True)


def render_scoring(scoring: dict):
    st.subheader("Scoring")

    st.metric("Overall Score", scoring.get("overall_score", "N/A"))

    scores = scoring.get("scores", {})
    if scores:
        df = pd.DataFrame(
            [{"Metric": pretty_score_name(k), "Score": v} for k, v in scores.items()]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

    if scoring.get("summary"):
        st.markdown("### Interpretation")
        st.write(scoring["summary"])


def render_risks(risks: dict):
    st.subheader("Risks")
    st.markdown(f"**Risk Level:** {risks.get('risk_level', 'N/A')}")
    for r in risks.get("top_risks", []):
        st.markdown(f"- {r}")


def render_scenarios(scenarios: dict):
    st.subheader("Future Scenarios")

    st.markdown("### Optimistic")
    st.write(scenarios.get("optimistic", ""))

    st.markdown("### Realistic")
    st.write(scenarios.get("realistic", ""))

    st.markdown("### Risky")
    st.write(scenarios.get("risky", ""))


def render_recommendations(recommendations: dict):
    st.subheader("Recommendations")

    st.markdown("### Verdict")
    st.write(recommendations.get("verdict", ""))

    st.markdown("### Next Steps")
    for step in recommendations.get("next_steps", []):
        st.markdown(f"- {step}")

    st.markdown("### MVP Focus")
    st.write(recommendations.get("mvp_focus", ""))

    st.markdown("### Validation Focus")
    st.write(recommendations.get("validation_focus", ""))

    if recommendations.get("strategic_note"):
        st.markdown("### Strategic Note")
        st.write(recommendations.get("strategic_note", ""))


def render_report(report: str):
    st.subheader("Full Report")
    st.markdown(report if report else "No report generated.")


warm_up_system()

st.title("🚀 VentureLens AI")
st.caption("AI-powered startup idea analysis grounded in real startup data")

st.markdown(
    """
VentureLens helps you:

- Structure your startup idea
- Find similar real-world startups
- Score opportunity potential
- Analyze risks
- Simulate future scenarios
- Generate actionable recommendations
"""
)

idea = st.text_area(
    "Describe your startup idea",
    height=180,
    placeholder="Example: An AI copilot that helps founders prepare investor updates, fundraising narratives, and KPI summaries."
)

if st.button("Analyze Idea", use_container_width=True):
    if not idea.strip():
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                result = run_full_analysis(idea)

                tabs = st.tabs([
                    "Structured Idea",
                    "Similar Startups",
                    "Scoring",
                    "Risks",
                    "Scenarios",
                    "Recommendations",
                    "Full Report",
                ])

                with tabs[0]:
                    st.subheader("Structured Idea")
                    render_kv_block(result.get("structured_idea", {}))

                with tabs[1]:
                    render_similar_startups(
                        result.get("similar_startups", []),
                        result.get("retrieval_summary", {}),
                    )

                with tabs[2]:
                    render_scoring(result.get("scoring", {}))

                with tabs[3]:
                    render_risks(result.get("risks", {}))

                with tabs[4]:
                    render_scenarios(result.get("scenarios", {}))

                with tabs[5]:
                    render_recommendations(result.get("recommendations", {}))

                with tabs[6]:
                    render_report(result.get("report", ""))

            except Exception as e:
                st.error(f"Error: {e}")
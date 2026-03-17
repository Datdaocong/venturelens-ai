import streamlit as st
import pandas as pd
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_modules.data_loader import load_ai_dataset


@st.cache_resource
def warm_up_system():
    load_ai_dataset()
    retrieve_similar_startups("AI startup", top_k=3)
    return True

warm_up_system()

_state = {
    "df": None,
    "vectorizer": None,
    "matrix": None,
    "text_col": None,
}


def _build_fallback_search_text(df: pd.DataFrame) -> pd.Series:
    for col in ["name", "industry", "sub_industry", "description", "hq_country", "hq_city"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)

    return (
        df["name"] + " | " +
        df["industry"] + " | " +
        df["sub_industry"] + " | " +
        df["description"] + " | " +
        df["hq_country"] + " | " +
        df["hq_city"]
    ).str.lower().str.strip()


def _get_text_series(df: pd.DataFrame):
    if "search_text" in df.columns and df["search_text"].astype(str).str.strip().ne("").any():
        return "search_text", df["search_text"].fillna("").astype(str)

    if "ai_context" in df.columns and df["ai_context"].astype(str).str.strip().ne("").any():
        return "ai_context", df["ai_context"].fillna("").astype(str)

    df["search_text"] = _build_fallback_search_text(df)
    return "search_text", df["search_text"]


def _init_engine(force_rebuild: bool = False):
    if (
        force_rebuild
        or _state["df"] is None
        or _state["vectorizer"] is None
        or _state["matrix"] is None
    ):
        df = load_ai_dataset(force_reload=force_rebuild)
        text_col, texts = _get_text_series(df)

        vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            stop_words="english",
        )
        matrix = vectorizer.fit_transform(texts)

        _state["df"] = df
        _state["vectorizer"] = vectorizer
        _state["matrix"] = matrix
        _state["text_col"] = text_col

        print(f"[Similarity] Initialized with text column: {text_col}")
        print(f"[Similarity] Matrix shape: {matrix.shape}")


def reset_similarity_engine():
    _state["df"] = None
    _state["vectorizer"] = None
    _state["matrix"] = None
    _state["text_col"] = None


def retrieve_similar_startups(query: str, top_k: int = 5) -> list[dict]:
    if not query or not query.strip():
        return []

    _init_engine()

    q_vec = _state["vectorizer"].transform([query.strip()])
    sims = cosine_similarity(q_vec, _state["matrix"]).flatten()

    top_idx = sims.argsort()[-top_k:][::-1]
    results = _state["df"].iloc[top_idx].copy()
    results["similarity"] = sims[top_idx]

    keep_cols = [
        "startup_id",
        "name",
        "description",
        "industry",
        "sub_industry",
        "hq_country",
        "hq_city",
        "status",
        "founded_year",
        "funding_round_count",
        "total_funding_usd",
        "has_acquisition",
        "has_ipo",
        "success_score",
        "outcome_label",
        "ai_context",
        "similarity",
    ]
    existing_cols = [c for c in keep_cols if c in results.columns]
    return results[existing_cols].to_dict("records")


def summarize_similar_startups(similar: list[dict]) -> dict:
    if not similar:
        return {
            "peer_count": 0,
            "avg_similarity": 0.0,
            "avg_success_score": 0.0,
            "avg_funding_round_count": 0.0,
            "avg_total_funding_usd": 0.0,
            "acquisition_rate": 0.0,
            "ipo_rate": 0.0,
            "top_outcomes": [],
            "top_industries": [],
        }

    df = pd.DataFrame(similar)

    for col in [
        "similarity",
        "success_score",
        "funding_round_count",
        "total_funding_usd",
        "has_acquisition",
        "has_ipo",
    ]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    outcome_counts = (
        df["outcome_label"].fillna("unknown").astype(str).value_counts().head(3).index.tolist()
        if "outcome_label" in df.columns else []
    )

    industry_counts = (
        df["industry"].fillna("unknown").astype(str).value_counts().head(3).index.tolist()
        if "industry" in df.columns else []
    )

    return {
        "peer_count": int(len(df)),
        "avg_similarity": round(float(df["similarity"].mean()), 4),
        "avg_success_score": round(float(df["success_score"].mean()), 2),
        "avg_funding_round_count": round(float(df["funding_round_count"].mean()), 2),
        "avg_total_funding_usd": round(float(df["total_funding_usd"].mean()), 2),
        "acquisition_rate": round(float(df["has_acquisition"].mean()), 2),
        "ipo_rate": round(float(df["has_ipo"].mean()), 2),
        "top_outcomes": outcome_counts,
        "top_industries": industry_counts,
    }
from ai_modules.full_analysis import run_full_analysis


st.set_page_config(
    page_title="VentureLens AI",
    page_icon="🚀",
    layout="wide",
)

# =========================
# Helpers
# =========================
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


# =========================
# UI
# =========================
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

analyze_btn = st.button("Analyze Idea", use_container_width=True)

# =========================
# Main Logic
# =========================
if analyze_btn:
    if not idea.strip():
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                result = run_full_analysis(idea)

                structured_idea = result.get("structured_idea", {})
                similar_startups = result.get("similar_startups", [])
                retrieval_summary = result.get("retrieval_summary", {})
                scoring = result.get("scoring", {})
                scenarios = result.get("scenarios", {})
                risks = result.get("risks", {})
                recommendations = result.get("recommendations", {})
                report = result.get("report", "")

                tabs = st.tabs([
                    "Structured Idea",
                    "Similar Startups",
                    "Scoring",
                    "Risks",
                    "Scenarios",
                    "Recommendations",
                    "Full Report",
                ])

                # =========================
                # Structured Idea
                # =========================
                with tabs[0]:
                    st.subheader("Structured Idea")
                    render_kv_block(structured_idea)

                # =========================
                # Similar Startups
                # =========================
                with tabs[1]:
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

                            rows.append({
                                "Metric": pretty_summary_name(k),
                                "Value": v
                            })

                        if rows:
                            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                    st.subheader("Top Similar Startups")

                    if similar_startups:
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
                    else:
                        st.info("No similar startups found.")

                # =========================
                # Scoring
                # =========================
                with tabs[2]:
                    st.subheader("Scoring")

                    st.metric("Overall Score", scoring.get("overall_score", "N/A"))

                    scores = scoring.get("scores", {})
                    if scores:
                        df = pd.DataFrame([
                            {"Metric": pretty_score_name(k), "Score": v}
                            for k, v in scores.items()
                        ])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    if scoring.get("summary"):
                        st.markdown("### Interpretation")
                        st.write(scoring["summary"])

                # =========================
                # Risks
                # =========================
                with tabs[3]:
                    st.subheader("Risks")

                    st.markdown(f"**Risk Level:** {risks.get('risk_level', 'N/A')}")

                    for r in risks.get("top_risks", []):
                        st.markdown(f"- {r}")

                # =========================
                # Scenarios
                # =========================
                with tabs[4]:
                    st.subheader("Future Scenarios")

                    st.markdown("### Optimistic")
                    st.write(scenarios.get("optimistic", ""))

                    st.markdown("### Realistic")
                    st.write(scenarios.get("realistic", ""))

                    st.markdown("### Risky")
                    st.write(scenarios.get("risky", ""))

                # =========================
                # Recommendations
                # =========================
                with tabs[5]:
                    st.subheader("Recommendations")

                    st.markdown(f"### Verdict")
                    st.write(recommendations.get("verdict", ""))

                    st.markdown("### Next Steps")
                    for step in recommendations.get("next_steps", []):
                        st.markdown(f"- {step}")

                    st.markdown("### MVP Focus")
                    st.write(recommendations.get("mvp_focus", ""))

                    st.markdown("### Validation Focus")
                    st.write(recommendations.get("validation_focus", ""))

                # =========================
                # Report
                # =========================
                with tabs[6]:
                    st.subheader("Full Report")
                    st.markdown(report)

            except Exception as e:
                st.error(f"Error: {e}")
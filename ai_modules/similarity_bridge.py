import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ai_modules.data_loader import load_ai_dataset

_state = {
    "df": None,
    "vectorizer": None,
    "matrix": None,
}


def _init_engine():
    if _state["df"] is None:
        df = load_ai_dataset()

        if "search_text" in df.columns and df["search_text"].astype(str).str.strip().ne("").any():
            texts = df["search_text"].fillna("").astype(str)
        elif "ai_context" in df.columns and df["ai_context"].astype(str).str.strip().ne("").any():
            texts = df["ai_context"].fillna("").astype(str)
        else:
            texts = (
                df["name"].fillna("").astype(str) + " "
                + df["industry"].fillna("").astype(str) + " "
                + df["description"].fillna("").astype(str)
            )

        vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(texts)

        _state["df"] = df
        _state["vectorizer"] = vectorizer
        _state["matrix"] = matrix

        print("[Similarity] Engine initialized")
        print(f"[Similarity] Dataset shape: {df.shape}")
        print(f"[Similarity] Matrix shape: {matrix.shape}")


def reset_similarity_engine():
    _state["df"] = None
    _state["vectorizer"] = None
    _state["matrix"] = None


def retrieve_similar_startups(query: str, top_k: int = 5) -> list[dict]:
    if not query or not query.strip():
        return []

    _init_engine()

    vec = _state["vectorizer"].transform([query.strip()])
    sims = cosine_similarity(vec, _state["matrix"]).flatten()

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

    numeric_cols = [
        "similarity",
        "success_score",
        "funding_round_count",
        "total_funding_usd",
        "has_acquisition",
        "has_ipo",
    ]
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    top_outcomes = (
        df["outcome_label"].fillna("unknown").astype(str).value_counts().head(3).index.tolist()
        if "outcome_label" in df.columns else []
    )

    top_industries = (
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
        "top_outcomes": top_outcomes,
        "top_industries": top_industries,
    }
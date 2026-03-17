import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ai_modules.data_loader import load_ai_dataset

_df = None
_vectorizer = None
_matrix = None


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


def _init_engine() -> None:
    global _df, _vectorizer, _matrix

    _df = load_ai_dataset()

    if "search_text" in _df.columns and _df["search_text"].astype(str).str.strip().ne("").any():
        texts = _df["search_text"].fillna("").astype(str)
    elif "ai_context" in _df.columns and _df["ai_context"].astype(str).str.strip().ne("").any():
        texts = _df["ai_context"].fillna("").astype(str)
    else:
        texts = _build_fallback_search_text(_df)
        _df["search_text"] = texts

    _vectorizer = TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        stop_words="english"
    )
    _matrix = _vectorizer.fit_transform(texts)


def retrieve_similar_startups(query: str, top_k: int = 5) -> list[dict]:
    global _vectorizer, _matrix, _df

    if _vectorizer is None or _matrix is None or _df is None:
        _init_engine()

    query = (query or "").strip()
    if not query:
        return []

    q_vec = _vectorizer.transform([query])
    sims = cosine_similarity(q_vec, _matrix).flatten()

    top_idx = sims.argsort()[-top_k:][::-1]
    results = _df.iloc[top_idx].copy()
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
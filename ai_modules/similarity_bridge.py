from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ai_modules.data_loader import load_dataset


# ===== GLOBAL CACHE =====
_df_cache: Optional[pd.DataFrame] = None
_vectorizer: Optional[TfidfVectorizer] = None
_tfidf_matrix = None


# ===== PREPROCESS =====
def _build_text_corpus(df: pd.DataFrame) -> pd.Series:
    """
    Combine text fields into one corpus for TF-IDF
    """
    text_cols = []

    if "description" in df.columns:
        text_cols.append(df["description"].fillna(""))

    if "industry" in df.columns:
        text_cols.append(df["industry"].fillna(""))

    if "sub_industry" in df.columns:
        text_cols.append(df["sub_industry"].fillna(""))

    if "ai_context" in df.columns:
        text_cols.append(df["ai_context"].fillna(""))

    if not text_cols:
        raise ValueError("No usable text columns found for similarity computation.")

    combined = text_cols[0]
    for col in text_cols[1:]:
        combined = combined + " " + col

    return combined.astype(str)


def _initialize():
    global _df_cache, _vectorizer, _tfidf_matrix

    if _df_cache is not None:
        return

    df = load_dataset()

    if df is None or df.empty:
        raise ValueError("Dataset is empty or failed to load.")

    df = df.copy().reset_index(drop=True)

    # Ensure required fallback columns exist
    if "name" not in df.columns:
        df["name"] = [f"Startup {i}" for i in range(len(df))]

    if "total_funding_usd" not in df.columns:
        df["total_funding_usd"] = 0

    if "success_score" not in df.columns:
        df["success_score"] = 0

    if "outcome_label" not in df.columns:
        df["outcome_label"] = "unknown"

    corpus = _build_text_corpus(df)

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english",
        ngram_range=(1, 2),
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)

    _df_cache = df
    _vectorizer = vectorizer
    _tfidf_matrix = tfidf_matrix


# ===== MAIN FUNCTION =====
def retrieve_similar_startups(user_idea: str, top_k: int = 5) -> pd.DataFrame:
    """
    Input: user idea text
    Output: DataFrame of top-k similar startups with similarity_score
    """

    _initialize()

    if not user_idea or not user_idea.strip():
        raise ValueError("User idea is empty.")

    query_vec = _vectorizer.transform([user_idea])

    similarities = cosine_similarity(query_vec, _tfidf_matrix).flatten()

    # Get top indices
    top_indices = similarities.argsort()[::-1][:top_k]

    result_df = _df_cache.iloc[top_indices].copy()

    # ===== IMPORTANT: STANDARDIZED COLUMN =====
    result_df["similarity_score"] = similarities[top_indices]

    # Sort again just to be safe
    result_df = result_df.sort_values("similarity_score", ascending=False)

    # ===== CLEAN OUTPUT =====
    keep_cols = [
        "name",
        "description",
        "industry",
        "sub_industry",
        "hq_country",
        "hq_city",
        "total_funding_usd",
        "success_score",
        "outcome_label",
        "similarity_score",
    ]

    existing_cols = [col for col in keep_cols if col in result_df.columns]
    result_df = result_df[existing_cols]

    result_df = result_df.reset_index(drop=True)

    return result_df
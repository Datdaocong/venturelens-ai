import pandas as pd


def safe_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).lower().strip()


def compute_similarity(idea_profile: dict, row: pd.Series) -> float:
    score = 0.0

    row_text = " ".join([
        safe_text(row.get("description", "")),
        safe_text(row.get("industry", "")),
        safe_text(row.get("business_model", "")),
        safe_text(row.get("subcategory", ""))
    ])

    for kw in idea_profile["keywords"]:
        if kw in row_text:
            score += 1.0

    for sector in idea_profile["sectors"]:
        if sector in row_text:
            score += 2.0

    for model in idea_profile["business_models"]:
        if model in row_text:
            score += 1.5

    return score


def retrieve_similar_startups(df: pd.DataFrame, idea_profile: dict, top_k: int = 5) -> list[dict]:
    scored_rows = []

    for _, row in df.iterrows():
        similarity = compute_similarity(idea_profile, row)
        scored_rows.append({
            "startup_name": row.get("startup_name", "Unknown"),
            "description": row.get("description", ""),
            "industry": row.get("industry", ""),
            "business_model": row.get("business_model", ""),
            "stage": row.get("stage", ""),
            "similarity": round(similarity, 2),
        })

    ranked = sorted(scored_rows, key=lambda x: x["similarity"], reverse=True)
    return ranked[:top_k]
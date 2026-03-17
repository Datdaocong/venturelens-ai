from __future__ import annotations

from pathlib import Path
import pandas as pd


IN_PATH = Path("data/processed/ai_startup_features.csv")
OUT_PATH = Path("data/processed/ai_startup_features_small.csv")


def main() -> None:
    df = pd.read_csv(IN_PATH, low_memory=False)

    required_cols = [
        "name",
        "industry",
        "description",
        "funding_round_count",
        "has_acquisition",
        "has_ipo",
        "success_score",
        "search_text",
        "ai_context",
    ]

    for col in required_cols:
        if col not in df.columns:
            if col in ["funding_round_count", "has_acquisition", "has_ipo", "success_score"]:
                df[col] = 0
            else:
                df[col] = ""

    df["name"] = df["name"].fillna("").astype(str)
    df["industry"] = df["industry"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    df["search_text"] = df["search_text"].fillna("").astype(str)
    df["ai_context"] = df["ai_context"].fillna("").astype(str)

    df["funding_round_count"] = pd.to_numeric(df["funding_round_count"], errors="coerce").fillna(0).astype(int)
    df["has_acquisition"] = pd.to_numeric(df["has_acquisition"], errors="coerce").fillna(0).astype(int)
    df["has_ipo"] = pd.to_numeric(df["has_ipo"], errors="coerce").fillna(0).astype(int)
    df["success_score"] = pd.to_numeric(df["success_score"], errors="coerce").fillna(0.0)

    # Keep rows that are actually useful for retrieval and reasoning
    small = df[
        (df["name"].str.strip() != "")
        & (
            (df["industry"].str.strip() != "")
            | (df["description"].str.len() > 20)
        )
        & (
            (df["description"].str.len() > 20)
            | (df["funding_round_count"] > 0)
            | (df["has_acquisition"] == 1)
            | (df["has_ipo"] == 1)
        )
    ].copy()

    if small.empty:
        print("Strict filter produced empty dataset. Falling back to lighter filter...")
        small = df[
            (df["name"].str.strip() != "")
            & (
                (df["industry"].str.strip() != "")
                | (df["description"].str.len() > 20)
            )
        ].copy()

    sort_cols = [c for c in ["success_score", "funding_round_count"] if c in small.columns]
    if sort_cols:
        small = small.sort_values(by=sort_cols, ascending=False)

    small = small.head(100000)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    small.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(f"Shape: {small.shape}")

    print("\nSample rows:")
    sample_cols = [
        c for c in [
            "name", "industry", "hq_country",
            "funding_round_count", "total_funding_usd",
            "success_score", "outcome_label"
        ] if c in small.columns
    ]
    print(small[sample_cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
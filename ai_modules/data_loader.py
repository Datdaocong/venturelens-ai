import os
import pandas as pd

SMALL_PATH = "data/processed/ai_startup_features_small.csv"
FULL_PATH = "data/processed/ai_startup_features.csv"

_df_cache = None


def load_ai_dataset() -> pd.DataFrame:
    global _df_cache

    if _df_cache is None:
        if os.path.exists(SMALL_PATH):
            path = SMALL_PATH
        elif os.path.exists(FULL_PATH):
            path = FULL_PATH
        else:
            raise FileNotFoundError(
                "No AI-ready dataset found. Expected one of:\n"
                f"- {SMALL_PATH}\n"
                f"- {FULL_PATH}"
            )

        df = pd.read_csv(path, low_memory=False)

        # đảm bảo các cột tối thiểu luôn tồn tại
        required_text_cols = [
            "startup_id",
            "name",
            "description",
            "industry",
            "sub_industry",
            "hq_country",
            "hq_city",
            "status",
            "search_text",
            "ai_context",
            "outcome_label",
        ]
        required_num_cols = [
            "founded_year",
            "funding_round_count",
            "total_funding_usd",
            "has_acquisition",
            "has_ipo",
            "success_score",
        ]

        for col in required_text_cols:
            if col not in df.columns:
                df[col] = ""

        for col in required_num_cols:
            if col not in df.columns:
                df[col] = 0

        for col in required_text_cols:
            df[col] = df[col].fillna("").astype(str)

        for col in required_num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        _df_cache = df
        print(f"[DataLoader] Loaded dataset from: {path}")
        print(f"[DataLoader] Shape: {_df_cache.shape}")

    return _df_cache.copy()
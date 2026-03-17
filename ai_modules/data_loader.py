import os
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
SMALL_PATH = DATA_DIR / "ai_startup_features_small.csv"
FULL_PATH = DATA_DIR / "ai_startup_features.csv"

_df_cache = {}


def _resolve_data_path() -> Path:
    mode = os.getenv("DATA_MODE", "small").strip().lower()

    if mode == "full":
        if FULL_PATH.exists():
            return FULL_PATH
        if SMALL_PATH.exists():
            return SMALL_PATH
    else:
        if SMALL_PATH.exists():
            return SMALL_PATH
        if FULL_PATH.exists():
            return FULL_PATH

    raise FileNotFoundError(
        "No AI-ready dataset found. Expected one of:\n"
        f"- {SMALL_PATH}\n"
        f"- {FULL_PATH}"
    )


def _postprocess(df: pd.DataFrame) -> pd.DataFrame:
    text_cols = [
        "startup_id",
        "name",
        "description",
        "industry",
        "sub_industry",
        "hq_country",
        "hq_city",
        "website",
        "status",
        "search_text",
        "ai_context",
        "outcome_label",
    ]

    numeric_cols = [
        "founded_year",
        "funding_round_count",
        "total_funding_usd",
        "acquisition_count",
        "ipo_count",
        "has_acquisition",
        "has_ipo",
        "is_success",
        "success_score",
        "log_total_funding",
        "startup_age_proxy",
    ]

    for col in text_cols:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)

    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def load_ai_dataset(force_reload: bool = False) -> pd.DataFrame:
    path = _resolve_data_path()
    cache_key = str(path.resolve())

    if force_reload or cache_key not in _df_cache:
        print(f"[DataLoader] Loading dataset from: {path}")
        df = pd.read_csv(path, low_memory=False)
        df = _postprocess(df)
        _df_cache[cache_key] = df
        print(f"[DataLoader] Loaded shape: {df.shape}")

    return _df_cache[cache_key]
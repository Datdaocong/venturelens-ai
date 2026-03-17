from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd


# ===== PATH CONFIG =====
DATA_DIR = Path("data/processed")

SMALL_PATH = DATA_DIR / "ai_startup_features_small.csv"
FULL_PATH = DATA_DIR / "ai_startup_features.csv"


# ===== CACHE =====
_df_cache: Optional[pd.DataFrame] = None


def _resolve_data_path() -> Path:
    """
    Choose dataset based on env variable DATA_MODE
    default = small
    """
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
        "No dataset found. Expected one of:\n"
        f"- {SMALL_PATH}\n"
        f"- {FULL_PATH}"
    )


def _basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning + ensure required columns exist
    """

    df = df.copy()

    # ===== TEXT =====
    if "description" in df.columns:
        df["description"] = df["description"].fillna("").astype(str)
    else:
        df["description"] = ""

    if "industry" in df.columns:
        df["industry"] = df["industry"].fillna("Unknown").astype(str)
    else:
        df["industry"] = "Unknown"

    if "sub_industry" in df.columns:
        df["sub_industry"] = df["sub_industry"].fillna("").astype(str)

    if "ai_context" in df.columns:
        df["ai_context"] = df["ai_context"].fillna("").astype(str)

    # ===== NAME =====
    if "name" not in df.columns:
        df["name"] = [f"Startup {i}" for i in range(len(df))]

    # ===== FUNDING =====
    if "total_funding_usd" not in df.columns:
        df["total_funding_usd"] = 0
    df["total_funding_usd"] = pd.to_numeric(df["total_funding_usd"], errors="coerce").fillna(0)

    # ===== SUCCESS SCORE =====
    if "success_score" not in df.columns:
        df["success_score"] = 0
    df["success_score"] = pd.to_numeric(df["success_score"], errors="coerce").fillna(0)

    # ===== OUTCOME =====
    if "outcome_label" not in df.columns:
        df["outcome_label"] = "unknown"
    df["outcome_label"] = df["outcome_label"].fillna("unknown").astype(str)

    return df


# ===== MAIN FUNCTION =====
def load_dataset(force_reload: bool = False) -> pd.DataFrame:
    """
    Load + cache dataset
    """

    global _df_cache

    if _df_cache is not None and not force_reload:
        return _df_cache

    path = _resolve_data_path()

    df = pd.read_csv(path)

    df = _basic_clean(df)

    _df_cache = df

    return df
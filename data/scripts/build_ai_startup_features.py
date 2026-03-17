import pandas as pd
import numpy as np
from pathlib import Path

SEARCH_PATH = Path("data/processed/startup_search_index.csv")
SIGNALS_PATH = Path("data/processed/startup_success_signals.csv")
OUT_PATH = Path("data/processed/ai_startup_features.csv")

search_df = pd.read_csv(SEARCH_PATH, low_memory=False)
signals_df = pd.read_csv(SIGNALS_PATH, low_memory=False)

search_df["startup_id"] = search_df["startup_id"].astype(str)
signals_df["startup_id"] = signals_df["startup_id"].astype(str)

merge_cols = [
    "startup_id",
    "funding_round_count",
    "total_funding_usd",
    "has_acquisition",
    "has_ipo",
    "success_score",
    "outcome_label",
]
existing_merge_cols = [c for c in merge_cols if c in signals_df.columns]

df = search_df.merge(
    signals_df[existing_merge_cols],
    on="startup_id",
    how="left",
)

text_cols = [
    "name",
    "description",
    "industry",
    "sub_industry",
    "hq_country",
    "hq_city",
    "status",
]

for col in text_cols:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].fillna("").astype(str).str.strip()

num_cols = [
    "founded_year",
    "funding_round_count",
    "total_funding_usd",
    "has_acquisition",
    "has_ipo",
    "success_score",
]
for col in num_cols:
    if col not in df.columns:
        df[col] = 0

df["founded_year"] = pd.to_numeric(df["founded_year"], errors="coerce")
df["funding_round_count"] = pd.to_numeric(df["funding_round_count"], errors="coerce").fillna(0).astype(int)
df["total_funding_usd"] = pd.to_numeric(df["total_funding_usd"], errors="coerce").fillna(0.0)
df["has_acquisition"] = pd.to_numeric(df["has_acquisition"], errors="coerce").fillna(0).astype(int)
df["has_ipo"] = pd.to_numeric(df["has_ipo"], errors="coerce").fillna(0).astype(int)
df["success_score"] = pd.to_numeric(df["success_score"], errors="coerce").fillna(0.0)

if "outcome_label" not in df.columns:
    df["outcome_label"] = "early_or_unknown"
df["outcome_label"] = df["outcome_label"].fillna("early_or_unknown").astype(str)

df["search_text"] = (
    df["name"] + " | " +
    df["industry"] + " | " +
    df["sub_industry"] + " | " +
    df["description"] + " | " +
    df["hq_country"] + " | " +
    df["hq_city"]
).str.lower().str.strip()

df["log_total_funding"] = np.log10(df["total_funding_usd"] + 1)
df["startup_age_proxy"] = 2026 - df["founded_year"]
df["startup_age_proxy"] = df["startup_age_proxy"].fillna(-1)

df["ai_context"] = (
    "startup: " + df["name"] +
    " | industry: " + df["industry"] +
    " | sub_industry: " + df["sub_industry"] +
    " | country: " + df["hq_country"] +
    " | city: " + df["hq_city"] +
    " | founded_year: " + df["founded_year"].fillna(-1).astype(int).astype(str) +
    " | status: " + df["status"] +
    " | funding_round_count: " + df["funding_round_count"].astype(str) +
    " | total_funding_usd: " + df["total_funding_usd"].astype(int).astype(str) +
    " | has_acquisition: " + df["has_acquisition"].astype(str) +
    " | has_ipo: " + df["has_ipo"].astype(str) +
    " | outcome_label: " + df["outcome_label"] +
    " | description: " + df["description"]
)

final_cols = [
    "startup_id",
    "name",
    "description",
    "industry",
    "sub_industry",
    "hq_country",
    "hq_city",
    "founded_year",
    "status",
    "search_text",
    "funding_round_count",
    "total_funding_usd",
    "log_total_funding",
    "has_acquisition",
    "has_ipo",
    "success_score",
    "outcome_label",
    "startup_age_proxy",
    "ai_context",
]

for col in final_cols:
    if col not in df.columns:
        df[col] = ""

df = df[final_cols].copy()

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Shape:", df.shape)
print(df.head())
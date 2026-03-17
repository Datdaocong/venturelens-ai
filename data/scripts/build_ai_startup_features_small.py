import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/ai_startup_features.csv")
OUT_PATH = Path("data/processed/ai_startup_features_small.csv")

df = pd.read_csv(IN_PATH, low_memory=False)

required_cols = [
    "name",
    "industry",
    "description",
    "funding_round_count",
    "has_acquisition",
    "has_ipo",
    "success_score",
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

df["funding_round_count"] = pd.to_numeric(df["funding_round_count"], errors="coerce").fillna(0).astype(int)
df["has_acquisition"] = pd.to_numeric(df["has_acquisition"], errors="coerce").fillna(0).astype(int)
df["has_ipo"] = pd.to_numeric(df["has_ipo"], errors="coerce").fillna(0).astype(int)
df["success_score"] = pd.to_numeric(df["success_score"], errors="coerce").fillna(0.0)

small = df[
    (df["name"].str.strip() != "") &
    (df["industry"].str.strip() != "") &
    (
        (df["description"].str.len() > 20) |
        (df["funding_round_count"] > 0) |
        (df["has_acquisition"] == 1) |
        (df["has_ipo"] == 1)
    )
].copy()

if small.empty:
    print("Filtered dataset is empty. Falling back to lighter filter...")
    small = df[
        (df["name"].str.strip() != "") &
        (df["industry"].str.strip() != "")
    ].copy()

sort_cols = [c for c in ["success_score", "funding_round_count"] if c in small.columns]
if sort_cols:
    small = small.sort_values(by=sort_cols, ascending=False)

small = small.head(100000)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
small.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Shape:", small.shape)
print(small.head())
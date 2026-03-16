import pandas as pd
from pathlib import Path

IN_PATH = Path("data/interim/startups_normalized.csv")
OUT_PATH = Path("data/processed/startup_search_index.csv")

df = pd.read_csv(IN_PATH)

for col in ["name", "description", "industry", "sub_industry", "hq_country", "hq_city"]:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].fillna("").astype(str)

df["search_text"] = (
    df["name"] + " | " +
    df["industry"] + " | " +
    df["sub_industry"] + " | " +
    df["description"] + " | " +
    df["hq_country"] + " | " +
    df["hq_city"]
).str.lower().str.strip()

df.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Shape:", df.shape)
print(df[["startup_id", "name", "search_text"]].head())
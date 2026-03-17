import pandas as pd
import re

RAW_PATH = "data/raw/startups_raw.csv"
PROCESSED_PATH = "data/processed/startups_clean.csv"

STANDARD_COLUMNS = {
    "startup_name": ["startup_name", "name", "company_name", "startup"],
    "description": ["description", "desc", "short_description", "overview", "long_description", "about"],
    "industry": ["industry", "sector", "category"],
    "business_model": ["business_model", "business", "model"],
    "funding_stage": ["funding_stage", "stage"],
    "status": ["status", "operating_status"],
    "country": ["country", "location_country"],
    "founded_year": ["founded_year", "founding_year", "year_founded", "founded"],
    "tags": ["tags", "keywords"]
}

def normalize_column_name(col):
    col = str(col).strip().lower()
    col = re.sub(r"[^a-z0-9]+", "_", col)
    col = re.sub(r"_+", "_", col).strip("_")
    return col

def find_matching_column(df_columns, candidates):
    for candidate in candidates:
        if candidate in df_columns:
            return candidate
    return None

def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value

def main():
    df = pd.read_csv(RAW_PATH)
    df.columns = [normalize_column_name(col) for col in df.columns]

    print("RAW COLUMNS:")
    print(df.columns.tolist())
    print("\nRAW SHAPE:", df.shape)
    print("\nRAW HEAD:")
    print(df.head(3))

    selected = {}

    print("\nCOLUMN MAPPING:")
    for standard_col, candidate_cols in STANDARD_COLUMNS.items():
        match = find_matching_column(df.columns, candidate_cols)
        print(f"{standard_col} -> {match}")
        if match:
            selected[standard_col] = df[match]
        else:
            selected[standard_col] = ""

    clean_df = pd.DataFrame(selected)

    text_cols = [
        "startup_name",
        "description",
        "industry",
        "business_model",
        "funding_stage",
        "status",
        "country",
        "tags"
    ]

    for col in text_cols:
        clean_df[col] = clean_df[col].apply(clean_text)

    if "founded_year" in clean_df.columns:
        clean_df["founded_year"] = pd.to_numeric(clean_df["founded_year"], errors="coerce")

    # fallback description nếu raw dataset không có cột mô tả
    empty_desc_mask = clean_df["description"].str.strip() == ""
    clean_df.loc[empty_desc_mask, "description"] = (
        clean_df.loc[empty_desc_mask, "industry"].fillna("").astype(str).str.strip() + " " +
        clean_df.loc[empty_desc_mask, "funding_stage"].fillna("").astype(str).str.strip() + " " +
        clean_df.loc[empty_desc_mask, "country"].fillna("").astype(str).str.strip()
    ).str.strip()

    clean_df["startup_name"] = clean_df["startup_name"].replace("", "unknown_startup")
    clean_df["industry"] = clean_df["industry"].replace("", "unknown")
    clean_df["business_model"] = clean_df["business_model"].replace("", "unknown")
    clean_df["status"] = clean_df["status"].replace("", "unknown")

    print("\nBEFORE FILTER:")
    print(clean_df.head(5))
    print("\nEMPTY DESCRIPTION COUNT:", (clean_df["description"].str.strip() == "").sum())
    print("TOTAL ROWS:", len(clean_df))

    clean_df = clean_df.drop_duplicates(subset=["startup_name", "description"])
    clean_df = clean_df[clean_df["description"].str.strip() != ""].copy()

    print("\nAFTER FILTER:")
    print(clean_df.head(5))
    print("FINAL SHAPE:", clean_df.shape)

    clean_df.to_csv(PROCESSED_PATH, index=False)
    print(f"\nSaved cleaned dataset to: {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
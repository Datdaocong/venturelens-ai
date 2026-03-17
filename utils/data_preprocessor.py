from pathlib import Path
import pandas as pd


RAW_PATH = Path("data/raw/startups_raw.csv")
PROCESSED_PATH = Path("data/processed/startups_clean.csv")

TARGET_COLUMNS = [
    "startup_id",
    "startup_name",
    "sector",
    "subsector",
    "country",
    "year_founded",
    "status",
    "funding_million",
    "valuation_million",
    "employee_count",
    "founder_count",
    "business_model",
    "market_type",
    "moat_type",
]

COLUMN_RENAME_MAP = {
    "startup": "startup_name",
    "name": "startup_name",
    "company": "startup_name",
    "industry": "sector",
    "founded_year": "year_founded",
    "founded": "year_founded",
    "funding": "funding_million",
    "valuation": "valuation_million",
    "employees": "employee_count",
    "founders": "founder_count",
}


def to_snake_case(text: str) -> str:
    return (
        text.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )


def normalize_status(value: str) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    mapping = {
        "active": "active",
        "operating": "active",
        "live": "active",
        "failed": "failed",
        "closed": "failed",
        "dead": "failed",
        "acquired": "acquired",
        "merged": "acquired",
        "struggling": "struggling",
    }

    return mapping.get(value, value)


def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower().replace(" ", "_")


def clean_numeric_column(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def preprocess_startup_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)

    # 1. clean column names
    df.columns = [to_snake_case(col) for col in df.columns]

    # 2. rename similar columns to target schema
    df = df.rename(columns=COLUMN_RENAME_MAP)

    # 3. add missing target columns
    for col in TARGET_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # 4. keep only target columns
    df = df[TARGET_COLUMNS]

    # 5. create startup_id if missing/empty
    if df["startup_id"].eq("").all():
        df["startup_id"] = range(1, len(df) + 1)

    # 6. normalize text columns
    text_cols = [
        "startup_name",
        "sector",
        "subsector",
        "country",
        "business_model",
        "market_type",
        "moat_type",
    ]
    for col in text_cols:
        df[col] = df[col].apply(normalize_text)

    # 7. normalize status separately
    df["status"] = df["status"].apply(normalize_status)

    # 8. numeric columns
    numeric_cols = [
        "year_founded",
        "funding_million",
        "valuation_million",
        "employee_count",
        "founder_count",
    ]
    for col in numeric_cols:
        df[col] = clean_numeric_column(df[col])

    # 9. save processed data
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    return df
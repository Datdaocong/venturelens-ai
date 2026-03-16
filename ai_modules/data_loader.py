from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


def load_startup_clean() -> pd.DataFrame:
    file_path = DATA_DIR / "startup_clean.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("startup_clean.csv is empty")

    return df


def load_startup_features() -> pd.DataFrame:
    file_path = DATA_DIR / "startup_features.csv"
    if not file_path.exists():
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    return df


def validate_startup_dataframe(df: pd.DataFrame) -> None:
    required_columns = [
        "startup_name",
        "description",
        "industry",
        "business_model",
        "stage"
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["description"].fillna("").str.strip().eq("").all():
        raise ValueError("All descriptions are empty")
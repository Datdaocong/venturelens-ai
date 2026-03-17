from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw")
OUT_PATH = Path("data/processed/ai_startup_features.csv")


def read_csv_flexible(path: Path) -> pd.DataFrame:
    last_err = None
    for enc in ["utf-8", "latin1", "cp1252"]:
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except Exception as e:
            last_err = e
    raise last_err


def first_existing(cols: list[str], candidates: list[str]) -> str | None:
    lower_map = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


def coalesce_text(df: pd.DataFrame, candidates: list[str], default: str = "") -> pd.Series:
    cols = [c for c in candidates if c in df.columns]
    if not cols:
        return pd.Series([default] * len(df), index=df.index, dtype="object")

    result = pd.Series([""] * len(df), index=df.index, dtype="object")
    for col in cols:
        vals = df[col].fillna("").astype(str).str.strip()
        result = np.where((pd.Series(result).astype(str).str.strip() == ""), vals, result)
        result = pd.Series(result, index=df.index, dtype="object")
    return result.fillna(default).astype(str)


def normalize_text_col(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip()


def build_objects_base() -> pd.DataFrame:
    path = RAW_DIR / "objects.csv"
    df = read_csv_flexible(path)

    # ----------------------------
    # Filter to company-like rows
    # ----------------------------
    entity_type_col = first_existing(
        list(df.columns),
        ["entity_type", "object_type", "type", "primary_role"]
    )

    if entity_type_col:
        tmp = df[entity_type_col].fillna("").astype(str).str.lower().str.strip()
        company_mask = (
            tmp.str.contains("company", na=False)
            | tmp.str.contains("organization", na=False)
            | tmp.str.contains("startup", na=False)
        )
        filtered = df[company_mask].copy()
        if not filtered.empty:
            df = filtered

    # ----------------------------
    # Pick core columns robustly
    # ----------------------------
    id_col = first_existing(list(df.columns), ["id", "uuid", "object_id"])
    name_col = first_existing(list(df.columns), ["name", "company_name"])
    industry_col = first_existing(list(df.columns), ["category_code", "category_list", "industry"])
    country_col = first_existing(list(df.columns), ["country_code", "hq_country", "country"])
    city_col = first_existing(list(df.columns), ["city", "hq_city"])
    status_col = first_existing(list(df.columns), ["status"])
    founded_col = first_existing(list(df.columns), ["founded_at", "founded_on", "founded_year"])
    homepage_col = first_existing(list(df.columns), ["homepage_url", "website", "domain"])

    if id_col is None or name_col is None:
        raise ValueError("objects.csv is missing a usable id/name column.")

    base = pd.DataFrame()
    base["startup_id"] = normalize_text_col(df[id_col])
    base["name"] = normalize_text_col(df[name_col])

    # Description: take best available text field
    base["description"] = coalesce_text(
        df,
        ["overview", "description", "short_description", "tag_line", "tagline"],
        default=""
    )

    # Industry + sub_industry
    if industry_col:
        base["industry"] = normalize_text_col(df[industry_col]).str.lower()
    else:
        base["industry"] = ""

    # Optional sub-industry from tags if any
    tag_col = first_existing(list(df.columns), ["tag_list", "tags", "sub_industry"])
    if tag_col:
        base["sub_industry"] = normalize_text_col(df[tag_col]).str.lower()
    else:
        base["sub_industry"] = ""

    base["hq_country"] = normalize_text_col(df[country_col]) if country_col else ""
    base["hq_city"] = normalize_text_col(df[city_col]) if city_col else ""
    base["status"] = normalize_text_col(df[status_col]).str.lower() if status_col else "unknown"
    base["website"] = normalize_text_col(df[homepage_col]) if homepage_col else ""

    # Founded year
    if founded_col:
        if pd.api.types.is_numeric_dtype(df[founded_col]):
            base["founded_year"] = pd.to_numeric(df[founded_col], errors="coerce")
        else:
            founded_dt = pd.to_datetime(df[founded_col], errors="coerce")
            base["founded_year"] = founded_dt.dt.year
    else:
        base["founded_year"] = np.nan

    # Existing funding signal directly from objects if present
    objects_funding_col = first_existing(list(df.columns), ["funding_total_usd", "total_funding_usd"])
    if objects_funding_col:
        base["objects_funding_total_usd"] = pd.to_numeric(df[objects_funding_col], errors="coerce").fillna(0.0)
    else:
        base["objects_funding_total_usd"] = 0.0

    # Existing funding round count directly from objects if present
    objects_rounds_col = first_existing(list(df.columns), ["funding_rounds", "investment_rounds"])
    if objects_rounds_col:
        base["objects_funding_round_count"] = pd.to_numeric(df[objects_rounds_col], errors="coerce").fillna(0).astype(int)
    else:
        base["objects_funding_round_count"] = 0

    base = base.dropna(subset=["startup_id", "name"])
    base = base[(base["startup_id"].str.strip() != "") & (base["name"].str.strip() != "")]
    base = base.drop_duplicates(subset=["startup_id"], keep="first")

    return base


def build_funding_agg() -> pd.DataFrame:
    path = RAW_DIR / "funding_rounds.csv"
    if not path.exists():
        return pd.DataFrame(columns=["startup_id", "funding_round_count", "total_funding_usd"])

    df = read_csv_flexible(path)
    key_col = first_existing(list(df.columns), ["object_id", "startup_id", "company_id", "funded_object_id"])
    amt_col = first_existing(list(df.columns), ["raised_amount_usd", "amount_usd", "funding_amount_usd"])

    if key_col is None:
        return pd.DataFrame(columns=["startup_id", "funding_round_count", "total_funding_usd"])

    df["startup_id"] = normalize_text_col(df[key_col])

    if amt_col:
        df["raised_amount_usd_clean"] = pd.to_numeric(df[amt_col], errors="coerce").fillna(0.0)
    else:
        df["raised_amount_usd_clean"] = 0.0

    agg = (
        df.groupby("startup_id", as_index=False)
        .agg(
            funding_round_count=("startup_id", "size"),
            total_funding_usd=("raised_amount_usd_clean", "sum"),
        )
    )
    return agg


def build_acquisition_agg() -> pd.DataFrame:
    path = RAW_DIR / "acquisitions.csv"
    if not path.exists():
        return pd.DataFrame(columns=["startup_id", "has_acquisition", "acquisition_count"])

    df = read_csv_flexible(path)
    key_col = first_existing(list(df.columns), ["acquired_object_id", "acquired_startup_id", "startup_id", "object_id"])
    if key_col is None:
        return pd.DataFrame(columns=["startup_id", "has_acquisition", "acquisition_count"])

    df["startup_id"] = normalize_text_col(df[key_col])

    agg = (
        df.groupby("startup_id", as_index=False)
        .agg(acquisition_count=("startup_id", "size"))
    )
    agg["has_acquisition"] = 1
    return agg


def build_ipo_agg() -> pd.DataFrame:
    path = RAW_DIR / "ipos.csv"
    if not path.exists():
        return pd.DataFrame(columns=["startup_id", "has_ipo", "ipo_count"])

    df = read_csv_flexible(path)
    key_col = first_existing(list(df.columns), ["object_id", "startup_id", "company_id"])
    if key_col is None:
        return pd.DataFrame(columns=["startup_id", "has_ipo", "ipo_count"])

    df["startup_id"] = normalize_text_col(df[key_col])

    agg = (
        df.groupby("startup_id", as_index=False)
        .agg(ipo_count=("startup_id", "size"))
    )
    agg["has_ipo"] = 1
    return agg


def build_final_features() -> pd.DataFrame:
    base = build_objects_base()
    funding = build_funding_agg()
    acq = build_acquisition_agg()
    ipo = build_ipo_agg()

    df = base.merge(funding, on="startup_id", how="left")
    df = df.merge(acq, on="startup_id", how="left")
    df = df.merge(ipo, on="startup_id", how="left")

    # Fill nulls from merged tables
    for col in ["funding_round_count", "total_funding_usd", "acquisition_count", "ipo_count"]:
        if col not in df.columns:
            df[col] = 0

    for col in ["has_acquisition", "has_ipo"]:
        if col not in df.columns:
            df[col] = 0

    df["funding_round_count"] = pd.to_numeric(df["funding_round_count"], errors="coerce").fillna(0).astype(int)
    df["total_funding_usd"] = pd.to_numeric(df["total_funding_usd"], errors="coerce").fillna(0.0)
    df["acquisition_count"] = pd.to_numeric(df["acquisition_count"], errors="coerce").fillna(0).astype(int)
    df["ipo_count"] = pd.to_numeric(df["ipo_count"], errors="coerce").fillna(0).astype(int)
    df["has_acquisition"] = pd.to_numeric(df["has_acquisition"], errors="coerce").fillna(0).astype(int)
    df["has_ipo"] = pd.to_numeric(df["has_ipo"], errors="coerce").fillna(0).astype(int)

    # Backfill from objects.csv direct signals if merged tables are missing
    df["funding_round_count"] = np.where(
        df["funding_round_count"] > 0,
        df["funding_round_count"],
        df["objects_funding_round_count"]
    ).astype(int)

    df["total_funding_usd"] = np.where(
        df["total_funding_usd"] > 0,
        df["total_funding_usd"],
        df["objects_funding_total_usd"]
    ).astype(float)

    # Backfill exits from status if available
    df["has_acquisition"] = np.where(
        (df["has_acquisition"] == 1) | (df["status"] == "acquired"),
        1,
        0
    ).astype(int)

    df["has_ipo"] = np.where(
        (df["has_ipo"] == 1) | (df["status"] == "ipo"),
        1,
        0
    ).astype(int)

    # Outcome label
    def outcome_label(row) -> str:
        if row["has_ipo"] == 1:
            return "ipo"
        if row["has_acquisition"] == 1:
            return "acquired"
        if str(row["status"]).strip().lower() == "closed":
            return "closed"
        if row["funding_round_count"] >= 2 or row["total_funding_usd"] >= 1_000_000:
            return "funded_growth"
        return "early_or_unknown"

    df["outcome_label"] = df.apply(outcome_label, axis=1)

    # Additional useful signals
    df["is_success"] = ((df["has_ipo"] == 1) | (df["has_acquisition"] == 1)).astype(int)

    # Human-friendly bins
    df["funding_level"] = pd.cut(
        df["total_funding_usd"],
        bins=[-1, 1e5, 1e6, 1e7, 1e8, np.inf],
        labels=["none_or_tiny", "low", "medium", "high", "mega"]
    ).astype(str)

    df["startup_stage"] = pd.cut(
        df["funding_round_count"],
        bins=[-1, 0, 1, 3, 10, np.inf],
        labels=["pre_funding", "early", "validated", "growth", "late"]
    ).astype(str)

    # Success score
    log_funding = np.log10(df["total_funding_usd"] + 1)

    df["success_score"] = (
        (df["funding_round_count"] * 0.8)
        + (log_funding * 1.2)
        + (df["has_acquisition"] * 4.0)
        + (df["has_ipo"] * 6.0)
    ).round(2)

    # Normalize text fields
    text_cols = ["name", "description", "industry", "sub_industry", "hq_country", "hq_city", "status", "website"]
    for col in text_cols:
        df[col] = normalize_text_col(df[col])

    df["industry"] = df["industry"].str.lower()
    df["sub_industry"] = df["sub_industry"].str.lower()
    df["status"] = df["status"].str.lower()

    # search_text
    df["search_text"] = (
        df["name"] + " | "
        + df["industry"] + " | "
        + df["sub_industry"] + " | "
        + df["description"] + " | "
        + df["hq_country"] + " | "
        + df["hq_city"]
    ).str.lower().str.strip()

    # ai_context
    founded_as_text = df["founded_year"].fillna(-1).astype("Int64").astype(str)
    df["ai_context"] = (
        "startup: " + df["name"]
        + " | industry: " + df["industry"]
        + " | sub_industry: " + df["sub_industry"]
        + " | country: " + df["hq_country"]
        + " | city: " + df["hq_city"]
        + " | founded_year: " + founded_as_text
        + " | status: " + df["status"]
        + " | funding_round_count: " + df["funding_round_count"].astype(str)
        + " | total_funding_usd: " + df["total_funding_usd"].round(0).astype(int).astype(str)
        + " | has_acquisition: " + df["has_acquisition"].astype(str)
        + " | has_ipo: " + df["has_ipo"].astype(str)
        + " | outcome_label: " + df["outcome_label"]
        + " | description: " + df["description"]
    )

    df["log_total_funding"] = np.log10(df["total_funding_usd"] + 1)
    df["startup_age_proxy"] = 2026 - pd.to_numeric(df["founded_year"], errors="coerce")
    df["startup_age_proxy"] = df["startup_age_proxy"].fillna(-1)

    final_cols = [
        "startup_id",
        "name",
        "description",
        "industry",
        "sub_industry",
        "hq_country",
        "hq_city",
        "founded_year",
        "website",
        "status",
        "funding_round_count",
        "total_funding_usd",
        "acquisition_count",
        "ipo_count",
        "has_acquisition",
        "has_ipo",
        "is_success",
        "funding_level",
        "startup_stage",
        "success_score",
        "outcome_label",
        "log_total_funding",
        "startup_age_proxy",
        "search_text",
        "ai_context",
    ]

    df = df[final_cols].copy()
    df = df.drop_duplicates(subset=["startup_id"], keep="first")

    return df


def main() -> None:
    df = build_final_features()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(f"Shape: {df.shape}")

    print("\nMissingness snapshot:")
    print(df[["industry", "description", "funding_round_count", "total_funding_usd", "outcome_label"]].isna().mean())

    print("\nOutcome distribution:")
    print(df["outcome_label"].value_counts(dropna=False).head(10))

    print("\nSample rows:")
    sample_cols = [
        "name", "industry", "hq_country",
        "funding_round_count", "total_funding_usd",
        "has_acquisition", "has_ipo",
        "success_score", "outcome_label"
    ]
    print(df[sample_cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
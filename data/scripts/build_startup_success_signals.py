import pandas as pd
from pathlib import Path

STARTUPS_PATH = Path("data/interim/startups_normalized.csv")
FUNDING_PATH = Path("data/raw/funding_rounds.csv")
ACQ_PATH = Path("data/raw/acquisitions.csv")
IPOS_PATH = Path("data/raw/ipos.csv")
OUT_PATH = Path("data/processed/startup_success_signals.csv")

# ----------------------------
# load startups master
# ----------------------------
startups = pd.read_csv(STARTUPS_PATH, low_memory=False)
startups["startup_id"] = startups["startup_id"].astype(str)

signals = startups[["startup_id", "name", "industry", "status"]].copy()

# ----------------------------
# funding rounds
# ----------------------------
funding = pd.read_csv(FUNDING_PATH, encoding="latin1", low_memory=False)
funding.columns = [c.strip() for c in funding.columns]

# map startup id column
funding_startup_col = None
for c in ["object_id", "startup_id", "company_id", "funded_object_id"]:
    if c in funding.columns:
        funding_startup_col = c
        break

# map amount column
funding_amount_col = None
for c in ["raised_amount_usd", "amount_usd", "raised_usd", "funding_amount_usd"]:
    if c in funding.columns:
        funding_amount_col = c
        break

if funding_startup_col is not None:
    funding[funding_startup_col] = funding[funding_startup_col].astype(str)

    funding_round_count = (
        funding.groupby(funding_startup_col)
        .size()
        .reset_index(name="funding_round_count")
    )

    if funding_amount_col is not None:
        funding[funding_amount_col] = pd.to_numeric(funding[funding_amount_col], errors="coerce")
        total_funding = (
            funding.groupby(funding_startup_col)[funding_amount_col]
            .sum(min_count=1)
            .reset_index(name="total_funding_usd")
        )
    else:
        total_funding = funding_round_count[[funding_startup_col]].copy()
        total_funding["total_funding_usd"] = pd.NA

    funding_signals = funding_round_count.merge(total_funding, on=funding_startup_col, how="left")
    funding_signals = funding_signals.rename(columns={funding_startup_col: "startup_id"})
else:
    funding_signals = pd.DataFrame(columns=["startup_id", "funding_round_count", "total_funding_usd"])

# ----------------------------
# acquisitions
# ----------------------------
acq = pd.read_csv(ACQ_PATH, encoding="latin1", low_memory=False)
acq.columns = [c.strip() for c in acq.columns]

acq_target_col = None
for c in ["acquired_object_id", "acquired_startup_id", "startup_id", "object_id"]:
    if c in acq.columns:
        acq_target_col = c
        break

if acq_target_col is not None:
    acq[acq_target_col] = acq[acq_target_col].astype(str)
    acq_signals = (
        acq.groupby(acq_target_col)
        .size()
        .reset_index(name="acquisition_count")
        .rename(columns={acq_target_col: "startup_id"})
    )
    acq_signals["has_acquisition"] = 1
else:
    acq_signals = pd.DataFrame(columns=["startup_id", "acquisition_count", "has_acquisition"])

# ----------------------------
# ipos
# ----------------------------
ipos = pd.read_csv(IPOS_PATH, encoding="latin1", low_memory=False)
ipos.columns = [c.strip() for c in ipos.columns]

ipo_startup_col = None
for c in ["object_id", "startup_id", "company_id"]:
    if c in ipos.columns:
        ipo_startup_col = c
        break

if ipo_startup_col is not None:
    ipos[ipo_startup_col] = ipos[ipo_startup_col].astype(str)
    ipo_signals = (
        ipos.groupby(ipo_startup_col)
        .size()
        .reset_index(name="ipo_count")
        .rename(columns={ipo_startup_col: "startup_id"})
    )
    ipo_signals["has_ipo"] = 1
else:
    ipo_signals = pd.DataFrame(columns=["startup_id", "ipo_count", "has_ipo"])

# ----------------------------
# merge all signals
# ----------------------------
signals = signals.merge(funding_signals, on="startup_id", how="left")
signals = signals.merge(acq_signals, on="startup_id", how="left")
signals = signals.merge(ipo_signals, on="startup_id", how="left")

# fill nulls
signals["funding_round_count"] = signals["funding_round_count"].fillna(0).astype(int)
signals["total_funding_usd"] = pd.to_numeric(signals["total_funding_usd"], errors="coerce").fillna(0)
signals["acquisition_count"] = signals["acquisition_count"].fillna(0).astype(int)
signals["ipo_count"] = signals["ipo_count"].fillna(0).astype(int)
signals["has_acquisition"] = signals["has_acquisition"].fillna(0).astype(int)
signals["has_ipo"] = signals["has_ipo"].fillna(0).astype(int)

# ----------------------------
# success score (simple heuristic)
# ----------------------------
signals["success_score"] = (
    signals["funding_round_count"] * 0.2
    + (signals["total_funding_usd"] / 1_000_000).clip(upper=50) * 0.05
    + signals["has_acquisition"] * 3
    + signals["has_ipo"] * 5
)

# optional outcome label
def outcome_label(row):
    if row["has_ipo"] == 1:
        return "ipo"
    if row["has_acquisition"] == 1:
        return "acquired"
    if row["status"] == "closed":
        return "closed"
    if row["funding_round_count"] >= 3 or row["total_funding_usd"] >= 10_000_000:
        return "funded_growth"
    return "early_or_unknown"

signals["outcome_label"] = signals.apply(outcome_label, axis=1)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
signals.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Shape:", signals.shape)
print(signals.head())
print("\nOutcome distribution:")
print(signals["outcome_label"].value_counts(dropna=False).head(10))
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/objects.csv")
OUT_PATH = Path("data/interim/startups_normalized.csv")

df = pd.read_csv(RAW_PATH, encoding="latin1")
print("Raw shape:", df.shape)
print("Columns:", df.columns.tolist())

# map linh hoạt theo schema thường gặp của Crunchbase snapshot
rename_map = {}

if "id" in df.columns:
    rename_map["id"] = "startup_id"
if "name" in df.columns:
    rename_map["name"] = "name"
if "category_code" in df.columns:
    rename_map["category_code"] = "industry"
if "country_code" in df.columns:
    rename_map["country_code"] = "hq_country"
if "city" in df.columns:
    rename_map["city"] = "hq_city"
if "homepage_url" in df.columns:
    rename_map["homepage_url"] = "website"
if "status" in df.columns:
    rename_map["status"] = "status"

df = df.rename(columns=rename_map)

# founded_year lấy từ founded_at nếu có
if "founded_at" in df.columns:
    founded = pd.to_datetime(df["founded_at"], errors="coerce")
    df["founded_year"] = founded.dt.year
elif "founded_on" in df.columns:
    founded = pd.to_datetime(df["founded_on"], errors="coerce")
    df["founded_year"] = founded.dt.year
else:
    df["founded_year"] = pd.NA

# description/sub_industry chưa có thì để trống
if "description" not in df.columns:
    df["description"] = pd.NA
if "sub_industry" not in df.columns:
    df["sub_industry"] = pd.NA

# chọn các cột theo schema VentureLens
required_cols = [
    "startup_id",
    "name",
    "description",
    "founded_year",
    "industry",
    "sub_industry",
    "hq_country",
    "hq_city",
    "website",
    "status",
]

for col in required_cols:
    if col not in df.columns:
        df[col] = pd.NA

df = df[required_cols].copy()

# clean cơ bản
df["name"] = df["name"].astype(str).str.strip()
df["industry"] = df["industry"].astype(str).str.strip().str.lower()
df["hq_country"] = df["hq_country"].astype(str).str.strip()
df["hq_city"] = df["hq_city"].astype(str).str.strip()
df["website"] = df["website"].astype(str).str.strip()
df["status"] = df["status"].astype(str).str.strip().str.lower()

# bỏ dòng rỗng
df = df[df["name"].notna()]
df = df[df["name"] != ""]
df = df[df["name"] != "nan"]

# bỏ trùng tương đối
df = df.drop_duplicates(subset=["startup_id"])
df = df.drop_duplicates(subset=["name", "hq_country", "founded_year"], keep="first")

# chuẩn hóa status
valid_status = {"operating": "active", "acquired": "acquired", "ipo": "ipo", "closed": "closed"}
df["status"] = df["status"].map(lambda x: valid_status.get(x, x if x in ["active", "acquired", "ipo", "closed"] else "unknown"))

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Normalized shape:", df.shape)
print(df.head())
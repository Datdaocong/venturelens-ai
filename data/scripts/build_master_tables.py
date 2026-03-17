import pandas as pd

df = pd.read_csv("data/interim/startups_normalized.csv")

# text field cho similarity
df["search_text"] = (
    df["name"].astype(str) + " " +
    df["industry"].astype(str) + " " +
    df["hq_country"].astype(str)
)

df.to_csv("data/processed/startup_search_index.csv", index=False)

print("Search index built:", df.shape)
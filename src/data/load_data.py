import pandas as pd

def load_startup_data(path="data/processed/startups_clean.csv"):
    df = pd.read_csv(path)
    return df
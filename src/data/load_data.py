import pandas as pd

DATA_PATH = "data/processed/startups_clean.csv"

def load_startup_data():
    return pd.read_csv(DATA_PATH)
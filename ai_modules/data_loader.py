import pandas as pd

DATA_PATH = "data/processed/ai_startup_features_small.csv"

_df_cache = None

def load_ai_dataset():
    global _df_cache
    if _df_cache is None:
        print("Loading AI dataset...")
        _df_cache = pd.read_csv(DATA_PATH, low_memory=False)
        print("Dataset loaded:", _df_cache.shape)
    return _df_cache
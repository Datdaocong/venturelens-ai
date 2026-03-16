import pandas as pd
import numpy as np

def clean_startup_data(input_path, output_path):

    df = pd.read_csv(input_path)

    # remove duplicates
    df = df.drop_duplicates()

    # fill missing values
    df["employees"] = df["employees"].fillna(df["employees"].median())

    # create derived metrics
    df["growth_rate"] = np.random.uniform(5, 40, len(df))
    df["market_size"] = np.random.uniform(1, 10, len(df))

    # startup scoring (for radar chart)
    df["product_score"] = np.random.uniform(5, 10, len(df))
    df["team_score"] = np.random.uniform(5, 10, len(df))
    df["traction_score"] = np.random.uniform(5, 10, len(df))
    df["innovation_score"] = np.random.uniform(5, 10, len(df))

    df.to_csv(output_path, index=False)

    return df
from utils.data_preprocessor import preprocess_startup_data

df = preprocess_startup_data()

print("Preprocessing completed.")
print(df.head())
print("\nColumns:")
print(list(df.columns))
print("\nShape:")
print(df.shape)
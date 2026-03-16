from src.data.load_data import load_startup_data
from src.analysis.startup_analyzer import StartupAnalyzer

df = load_startup_data()

analyzer = StartupAnalyzer(df)
df = analyzer.calculate_score()
df = analyzer.investment_signal()
ranked = analyzer.rank_startups()

print(ranked[["startup_name", "startup_score", "signal"]].head())
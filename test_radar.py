from src.data.load_data import load_startup_data
from src.analysis.startup_analyzer import StartupAnalyzer
from src.visualization.radar_chart import plot_startup_radar

df = load_startup_data()

analyzer = StartupAnalyzer(df)
df = analyzer.calculate_score()
df = analyzer.investment_signal()

startup = df[df["startup_name"] == "Notion"].iloc[0]

plot_startup_radar(startup)
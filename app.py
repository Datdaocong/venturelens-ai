import streamlit as st

from src.data.load_data import load_startup_data
from src.analysis.startup_analyzer import StartupAnalyzer
from src.visualization.radar_chart import plot_startup_radar

st.title("🚀 VentureLens - Startup Analyzer")

df = load_startup_data()

analyzer = StartupAnalyzer(df)
df = analyzer.calculate_score()
df = analyzer.investment_signal()

startup_list = df["startup_name"].tolist()

selected = st.selectbox(
    "Select a startup",
    startup_list
)

startup = df[df["startup_name"] == selected].iloc[0]

st.subheader("Startup Evaluation")

col1, col2 = st.columns(2)

col1.metric("Startup Score", round(startup["startup_score"],2))
col2.metric("Investment Signal", startup["signal"])

st.subheader("Radar Analysis")

analysis_text = analyzer.generate_analysis(startup)

st.markdown(analysis_text)

fig = plot_startup_radar(startup)

st.pyplot(fig)

st.subheader("Startup Data")

st.dataframe(startup)
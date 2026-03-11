from ai_modules.scoring_engine import score_startup
import streamlit as st
from ai_modules.idea_structurer import structure_startup_idea
st.set_page_config(page_title="VentureLens AI", page_icon="🚀", layout="wide")

st.title("🚀 VentureLens AI")
st.subheader("AI Startup Idea Analyzer and Scenario Simulator")

startup_idea = st.text_area(
    "Describe your startup idea:",
    placeholder="Example: An AI platform that helps students automatically summarize lecture recordings...",
    height=180
)

if st.button("Analyze Idea"):
    if startup_idea.strip():
        with st.spinner("Structuring your startup idea..."):
            structured_idea = structure_startup_idea(startup_idea)

            scoring = score_startup(structured_idea)

        st.success("Idea analyzed successfully!")

        st.write("## Structured Startup Idea")
        st.json(structured_idea)

        st.write("## Startup Score")
        st.json(scoring)        
    else:
        st.warning("Please enter a startup idea first.")



import streamlit as st

st.set_page_config(page_title="VentureLens AI", page_icon="🚀", layout="wide")

st.title("🚀 VentureLens AI")
st.subheader("AI Startup Idea Analyzer and Scenario Simulator")

startup_idea = st.text_area(
    "Describe your startup idea:",
    placeholder="Example: An AI platform that helps students automatically summarize lecture recordings..."
)

if st.button("Analyze Idea"):
    if startup_idea.strip():
        st.success("Idea received successfully!")
        st.write("### Your Idea")
        st.write(startup_idea)
    else:
        st.warning("Please enter a startup idea first.")
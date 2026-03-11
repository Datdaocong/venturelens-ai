import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()


def get_gemini_client():
    api_key = None

    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in Streamlit secrets or .env")

    return genai.Client(api_key=api_key)
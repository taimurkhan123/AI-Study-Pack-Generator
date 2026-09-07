import os
import streamlit as st
from google import genai

MODEL = "gemini-3.6-flash"

def get_api_key():
    # Local development: .streamlit/secrets.toml
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    # Optional fallback for environment variables.
    return os.getenv("GEMINI_API_KEY")

def get_client():
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .streamlit/secrets.toml "
            "locally or Streamlit Cloud Secrets when deploying."
        )
    return genai.Client(api_key=api_key)

def generate_stage(prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text

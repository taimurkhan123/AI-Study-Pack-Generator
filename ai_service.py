import os
import time
import streamlit as st
from google import genai
from google.genai.errors import APIError

# Use the current supported Gemini 3.6 Flash model
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

def generate_stage(prompt: str, retries: int = 3, delay: float = 2.0) -> str:
    """Generates content and automatically retries if Google servers are busy."""
    client = get_client()

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text

        except APIError as e:
            # If Google server is overloaded (503) or rate limited (429), pause and retry
            if getattr(e, "code", None) in [503, 429] or "high demand" in str(e).lower():
                if attempt < retries - 1:
                    time.sleep(delay * (2 ** attempt))  # Pause 2s, 4s, 8s...
                    continue
            raise e

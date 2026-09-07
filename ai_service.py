import os
import time
import streamlit as st
from google import genai
from google.genai.errors import APIError, ServerError

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

def generate_stage(prompt: str, retries: int = 5, delay: float = 3.0) -> str:
    """Generates content with robust retries for temporary server overloads."""
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

        except (APIError, ServerError, Exception) as e:
            error_str = str(e).lower()
            is_overloaded = (
                "503" in error_str 
                or "unavailable" in error_str 
                or "high demand" in error_str
                or "429" in error_str
                or "resource_exhausted" in error_str
            )

            # If Google servers are busy, wait longer and retry
            if is_overloaded and attempt < retries - 1:
                wait_time = delay * (2 ** attempt)  # Pauses: 3s, 6s, 12s, 24s...
                time.sleep(wait_time)
                continue
            
            # If it's a different error or out of retries, raise it
            raise e

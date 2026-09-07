import os
import re
import time
import streamlit as st
from google import genai
from google.genai.errors import APIError, ClientError, ServerError

# Updated model to gemini-3.8-flash
MODEL = "gemini-3.8-flash"

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.getenv("GEMINI_API_KEY")

def get_client():
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .streamlit/secrets.toml "
            "locally or Streamlit Cloud Secrets when deploying."
        )
    return genai.Client(api_key=api_key)

def extract_retry_delay(error_msg: str) -> float:
    """Extracts suggested retry delay from 429 error messages."""
    match = re.search(r"retry in (\d+\.?\d*)s", error_msg, re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1.0
    return 10.0

def generate_stage(prompt: str, retries: int = 3) -> str:
    client = get_client()

    for attempt in range(retries):
        try:
            # Using client.interactions.create with gemini-3.8-flash
            interaction = client.interactions.create(
                model=MODEL,
                input=prompt
            )

            # Retrieve text output from interaction.outputs
            if hasattr(interaction, "outputs") and interaction.outputs:
                text = getattr(interaction.outputs[-1], "text", None)
            else:
                text = getattr(interaction, "output_text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text

        except (APIError, ClientError, ServerError) as e:
            error_str = str(e)

            # Handle rate limits (429) & server overloads (503) automatically
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "503" in error_str:
                if attempt < retries - 1:
                    wait_time = extract_retry_delay(error_str)
                    st.toast(f"⏳ Rate limit reached. Retrying in {int(wait_time)} seconds...", icon="⏱️")
                    time.sleep(wait_time)
                    continue

            raise e

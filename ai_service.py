import os
import time

import streamlit as st
from google import genai
from google.genai import errors


MODEL = "gemini-3.6-flash"


def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    return os.getenv("GEMINI_API_KEY")


def get_client():
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to "
            ".streamlit/secrets.toml locally or Streamlit Cloud Secrets."
        )

    return genai.Client(api_key=api_key)


def generate_stage(prompt: str) -> str:
    client = get_client()

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text

        except errors.ServerError as e:
            # Gemini 503 = temporary server/model overload
            if getattr(e, "code", None) == 503:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt

                    st.warning(
                        f"Gemini is temporarily busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                else:
                    raise RuntimeError(
                        "Gemini is currently overloaded after multiple retries. "
                        "Please try again in a few minutes."
                    ) from e

            else:
                raise

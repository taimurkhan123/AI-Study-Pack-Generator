import os
import streamlit as st
from google import genai
from google.genai import types


MODEL = "gemini-3.6-flash"


def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    return os.getenv("GEMINI_API_KEY")


def get_client():
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )

    return genai.Client(api_key=api_key)


def generate_stage(prompt: str) -> str:

    client = get_client()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1000
        )
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text

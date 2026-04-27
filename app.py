import streamlit as st
from google import genai
from tweets import TWEETS

# Load Gemini key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet or message")

def build_style():
    return "\n".join([f"- {t}" for t in TWEETS])

def rewrite(text):
    prompt = f"""
You are a political communications assistant.

Rewrite the input in the exact tone and style of the examples below.

STYLE EXAMPLES:
{build_style()}

RULES:
- Do NOT add new facts
- Keep meaning identical
- Use short, confident political sentences
- Avoid generic phrases like "moving forward" or "together we can"
- Do NOT sound like AI

INPUT:
{text}

OUTPUT:
Return only the rewritten version.
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text

if st.button("Rewrite with Gemini"):

    if not text.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("Rewriting..."):
            result = rewrite(text)

        st.subheader("Original")
        st.write(text)

        st.subheader("Rewritten")
        st.write(result)

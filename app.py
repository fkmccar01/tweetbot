import streamlit as st
from tweets import TWEETS
from google import genai

# Load key safely from Streamlit secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet here")

def build_style():
    return "\n".join([f"- {t}" for t in TWEETS])

def rewrite(user_text):
    prompt = f"""
You are a political communications assistant.

Rewrite the input in a clear political voice.

STYLE EXAMPLES:
{build_style()}

RULES:
- Do NOT change meaning
- Do NOT add new facts
- Make it sound like polished political messaging
- Short, confident sentences

INPUT:
{user_text}

OUTPUT:
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text

if st.button("Rewrite with Gemini"):
    if not text:
        st.warning("Enter text first")
    else:
        st.subheader("Original")
        st.write(text)

        st.subheader("Rewritten")
        st.write(rewrite(text))

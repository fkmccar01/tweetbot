import streamlit as st
from google import genai
from tweets import TWEETS  # <-- your external style database

# ----------------------------
# GEMINI CLIENT
# ----------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ----------------------------
# STYLE BUILDER
# ----------------------------
def build_style():
    return "\n".join([f"- {t}" for t in TWEETS])

# ----------------------------
# PROMPT ENGINE
# ----------------------------
def rewrite_text(user_text):

    prompt = f"""
You are a senior political communications assistant who has to write tweets in the voice and style of your boss, a congressman.

Rewrite the input text in the exact voice, cadence, and rhetorical style of the speaker.

STYLE EXAMPLES:
{build_style()}

RULES:
- Preserve meaning exactly
- Do NOT add new facts or claims
- Match tone, cadence, and sentence structure
- Use short, confident sentences
- Avoid generic political phrases (e.g. "moving forward", "together we can")
- Do NOT sound like an AI assistant

STRUCTURE:
- short claim → justification → implication or call to action
- sometimes contrast framing (what is vs what should be)

INPUT:
{user_text}

OUTPUT:
Return only the rewritten text.
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet or message")

if st.button("Rewrite with Gemini"):

    if not text.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("Rewriting..."):
            result = rewrite_text(text)

        st.subheader("Original")
        st.write(text)

        st.subheader("Rewritten")
        st.write(result)

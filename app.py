import streamlit as st
from google import genai
from tweets import TWEETS

# ----------------------------
# LOAD API KEY SAFELY
# ----------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets")
    st.stop()

client = genai.Client(api_key=API_KEY)

# ----------------------------
# STYLE BUILDER
# ----------------------------
def build_style():
    return "\n".join([f"- {t}" for t in TWEETS])

# ----------------------------
# GEMINI REWRITE FUNCTION
# ----------------------------
def rewrite_text(user_text):

    prompt = f"""
You are a senior political communications assistant who drafts tweets for your boss, a congressman.

Rewrite the input text in the exact voice, cadence, and rhetorical style of the speaker.

STYLE EXAMPLES:
{build_style()}

RULES:
- Preserve meaning exactly
- Do NOT add new facts or claims
- Use short, confident political sentences, but with a slight casual speaking/conversational tone
- Avoid generic phrases like "moving forward", "together we can"
- Do NOT sound like an AI assistant
- Make it sound like real political messaging

INPUT:
{user_text}

OUTPUT:
Return only the rewritten text.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ✅ stable SDK-supported model
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"ERROR CALLING GEMINI: {e}"

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="GregBot", page_icon="🧠")

st.title("GregBot - Tweet Enhancement Tool")

text = st.text_area("Paste a draft tweet or message")

if st.button("GregBot this!"):

    if not text.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("GregBot is working..."):
            result = rewrite_text(text)

        st.subheader("Original")
        st.write(text)

        st.subheader("GregBot's Version")
        st.write(result)

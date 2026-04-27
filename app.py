import streamlit as st
from google import genai
from tweets import TWEETS

# ----------------------------
# SAFE API KEY LOADING
# ----------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Missing GEMINI_API_KEY in Streamlit secrets")
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
You are a senior political communications assistant.

Rewrite the input text in the exact voice, cadence, and rhetorical style of the speaker.

STYLE EXAMPLES:
{build_style()}

RULES:
- Preserve meaning exactly
- Do NOT add new facts or claims
- Use short, confident political sentences
- Avoid generic phrases (e.g. "moving forward", "together we can")
- Do NOT sound like an AI assistant
- Make it sound like a real political message

INPUT:
{user_text}

OUTPUT:
Return only the rewritten text.
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"ERROR CALLING GEMINI: {e}"

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="TweetBot", page_icon="🧠")

st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet or message")

if st.button("Rewrite with Gemini"):

    if not text.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("Rewriting with Gemini..."):
            result = rewrite_text(text)

        st.subheader("Original")
        st.write(text)

        st.subheader("Rewritten")
        st.write(result)

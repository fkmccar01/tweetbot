import streamlit as st
from tweets import TWEETS

st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet here")

def build_style():
    return "\n".join([f"- {t}" for t in TWEETS])

if st.button("Rewrite (style-based)"):
    st.subheader("Input")
    st.write(text)

    st.subheader("Style Reference (what we imitate)")
    st.write(build_style())

    st.subheader("Output")
    st.write("👉 Next step: we connect Gemini here to actually rewrite this")

import streamlit as st

st.title("TweetBot - Political Rewrite Tool")

text = st.text_area("Paste a draft tweet here")

if st.button("Rewrite"):
    st.write("You entered:")
    st.write(text)

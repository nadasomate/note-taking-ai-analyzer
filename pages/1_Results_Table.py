import streamlit as st 
from utils import search_apps
import pandas as pd

st.title("Search Results – Google Play Apps")

# User input field
query = st.text_input("Enter a keyword to search for apps:", value="note taking ai")

# Number of apps to retrieve
n = st.slider("Number of apps to display:", min_value=5, max_value=30, value=10)

# Trigger search
if st.button("Search"):
    with st.spinner("Searching..."):
        df = search_apps(query, n)
        if not df.empty:
            st.success(f"{len(df)} apps found for: '{query}'")
            st.dataframe(df)
        else:
            st.warning("No apps found.")

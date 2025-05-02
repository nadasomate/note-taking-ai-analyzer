import streamlit as st 
from utils import search_apps
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Google Play App Visualizations")

# User input
query = st.text_input("Enter a keyword to analyze apps:", value="note taking ai")
n = st.slider("Number of apps to analyze:", min_value=5, max_value=30, value=10)

# Generate charts
if st.button("Generate Charts"):
    with st.spinner("Loading data..."):
        df = search_apps(query, n)

        if df.empty:
            st.warning("No apps found.")
        else:
            st.success(f"{len(df)} apps found.")

            # Bar chart: App score distribution
            st.subheader("Score Distribution")
            fig1, ax1 = plt.subplots()
            df['score'].value_counts().sort_index().plot(kind='bar', ax=ax1)
            ax1.set_xlabel("Rating")
            ax1.set_ylabel("Number of apps")
            st.pyplot(fig1)

            # Pie chart: Free vs Paid
            st.subheader("Free vs Paid Distribution")
            pie_data = df['free'].value_counts()
            fig2, ax2 = plt.subplots()
            labels = pie_data.index.map(lambda x: "Free" if x else "Paid")
            ax2.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=90)            
            ax2.axis('equal')
            st.pyplot(fig2)

            # Bar chart: Genre distribution
            st.subheader("Genre Distribution")
            fig3, ax3 = plt.subplots()
            df['genre'].value_counts().plot(kind='barh', ax=ax3)
            ax3.set_xlabel("Number of apps")
            st.pyplot(fig3)

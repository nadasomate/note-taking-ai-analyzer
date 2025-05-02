import streamlit as st
from utils import search_apps, get_reviews, analyze_reviews
import pandas as pd

st.title("Sentiment Analysis of User Reviews")

# User input
query = st.text_input("Enter a keyword to search for apps:", value="note taking ai")
n = st.slider("Number of apps to analyze:", min_value=5, max_value=20, value=5)

if st.button("Analyze Sentiments"):
    with st.spinner("Loading data and fetching reviews..."):
        df = search_apps(query, n)

        if df.empty:
            st.warning("No apps found.")
        else:
            app_sentiments = []

            for _, row in df.iterrows():
                app_id = row['app_id']
                reviews = get_reviews(app_id, count=10)

                if not reviews:
                    app_sentiments.append({
                        'App': row['title'],
                        'Positive': 0,
                        'Negative': 0
                    })
                    continue

                results = analyze_reviews(reviews)

                # Count positive and negative reviews
                pos = sum(1 for r in results if r['label'] == 'POSITIVE')
                neg = sum(1 for r in results if r['label'] == 'NEGATIVE')

                app_sentiments.append({
                    'App': row['title'],
                    'Positive': pos,
                    'Negative': neg
                })

            # Display table and chart
            sentiment_df = pd.DataFrame(app_sentiments)
            st.subheader("Sentiment Scores by Application")
            st.dataframe(sentiment_df)
            st.bar_chart(sentiment_df.set_index("App"))

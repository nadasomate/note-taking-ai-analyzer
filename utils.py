from google_play_scraper import search, app, reviews, Sort 
import pandas as pd
from transformers import pipeline

# Function to search for apps
def search_apps(query, n=10):
    """
    Searches for apps related to a keyword on the Google Play Store
    and returns a DataFrame with key information.
    """
    results = search(query, lang='en', country='us')

    data = []
    for a in results[:n]:
        app_id = a['appId']
        details = app(app_id, lang='en', country='us')
        data.append({
            'app_id': app_id,
            'title': details['title'],
            'description': details['description'],
            'score': details['score'],
            'installs': details['installs'],
            'free': details['free'],
            'genre': details['genre']
        })
    return pd.DataFrame(data)
# Load HuggingFace sentiment analysis model (only once)
sentiment_analyzer = pipeline("sentiment-analysis")
# Retrieve reviews for a given app
def get_reviews(app_id, count=10):
    """
    Retrieves a list of user review texts for a given app.
    """
    result, _ = reviews(app_id, lang='en', country='us', count=count, sort=Sort.NEWEST)
    return [r['content'] for r in result]
# Apply sentiment analysis to a list of texts
def analyze_reviews(review_list):
    """
    Applies the HuggingFace sentiment analysis model to a list of texts.
    Returns a list of results with label (POSITIVE / NEGATIVE) and score.
    """
    sentiments = sentiment_analyzer(review_list)
    return sentiments
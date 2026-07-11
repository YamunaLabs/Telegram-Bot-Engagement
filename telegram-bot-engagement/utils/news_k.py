import requests

import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY_HERE")  # 👈 Set NEWS_API_KEY in .env or replace here

def fetch_top_headlines():
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "language": "en",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY,
        }
        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        headlines = [a["title"] for a in articles if "title" in a]
        return headlines
    except Exception as e:
        print("[NewsAPI Error]:", e)
        return []

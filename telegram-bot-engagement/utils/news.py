import random
import requests

NEWS_LINKS = []

import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY_HERE")  # 👈 Set NEWS_API_KEY in .env or replace here

def fetch_news_links(topic):
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": NEWS_API_KEY,
            "pageSize": 5
        }
        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        links = [article["url"] for article in articles if "url" in article]

        if links:
            return random.sample(links, k=min(2, len(links)))
        else:
            return random.sample(NEWS_LINKS, k=2)

    except Exception as e:
        print("[NewsAPI Error]:", e)
        return random.sample(NEWS_LINKS, k=2)  # fallback to static links

def get_trending_article_snippet():
    return "Trending: AI is transforming the way schools operate globally."

def fetch_image_link(topic):
    return f"https://source.unsplash.com/400x300/?{topic.replace(' ', '-')}-news"

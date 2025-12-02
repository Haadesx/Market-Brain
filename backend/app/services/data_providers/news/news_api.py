import httpx
from datetime import datetime
from typing import List, Dict, Any
from app.services.data_providers.base import BaseNewsProvider
import os

class NewsAPIProvider(BaseNewsProvider):
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")

    async def fetch_news(self, symbol: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        params = {
            "q": symbol,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": self.api_key
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        articles = []
        for item in data.get("articles", []):
            articles.append({
                "published_at": datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
                "title": item["title"],
                "url": item["url"],
                "source": item["source"]["name"],
                "content": item["description"] or item["content"],
                "sentiment_score": 0.0, # Placeholder
                "sentiment_label": "neutral" # Placeholder
            })
        
        return articles

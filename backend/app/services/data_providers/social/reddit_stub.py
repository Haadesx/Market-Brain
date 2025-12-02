from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.data_providers.base import BaseSocialProvider
import random

class RedditStubProvider(BaseSocialProvider):
    async def fetch_posts(self, symbol: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        # Generate fake reddit posts
        posts = []
        current_time = start_date
        while current_time <= end_date:
            if random.random() > 0.7: # 30% chance of a post per hour
                posts.append({
                    "id": f"reddit_{int(current_time.timestamp())}",
                    "platform": "reddit",
                    "created_at": current_time,
                    "content": f"I think ${symbol} is going to the moon! 🚀",
                    "author": "diamond_hands_ape",
                    "sentiment_score": random.uniform(-1, 1)
                })
            current_time += timedelta(hours=1)
        return posts

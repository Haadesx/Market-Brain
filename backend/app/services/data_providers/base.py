from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

class BaseMarketDataProvider(ABC):
    @abstractmethod
    async def get_historical_ohlcv(self, symbol: str, interval: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Fetch historical OHLCV data.
        Returns DataFrame with columns: [time, open, high, low, close, volume]
        """
        pass

    @abstractmethod
    async def get_realtime_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch real-time quote.
        """
        pass

class BaseNewsProvider(ABC):
    @abstractmethod
    async def fetch_news(self, symbol: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch news articles.
        Returns list of dicts: {title, url, published_at, source, content, ...}
        """
        pass

class BaseSocialProvider(ABC):
    @abstractmethod
    async def fetch_posts(self, symbol: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch social media posts.
        Returns list of dicts: {id, platform, content, author, created_at, ...}
        """
        pass

from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.market import MarketData, NewsArticle
from app.services.data_providers.market.alpha_vantage import AlphaVantageProvider
from app.services.data_providers.news.news_api import NewsAPIProvider
from app.services.data_providers.social.reddit_stub import RedditStubProvider

class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.market_provider = AlphaVantageProvider()
        self.news_provider = NewsAPIProvider()
        self.social_provider = RedditStubProvider()

    async def ingest_market_data(self, symbol: str, start_date: datetime, end_date: datetime):
        df = await self.market_provider.get_historical_ohlcv(symbol, "1d", start_date, end_date)
        if df.empty:
            return 0
        
        # Bulk insert (upsert logic needed for production, simple insert for now)
        # In a real app, we'd use postgres ON CONFLICT DO UPDATE
        records = df.to_dict(orient="records")
        for record in records:
            # Check if exists (inefficient, but safe for now)
            stmt = select(MarketData).where(
                MarketData.symbol == record["symbol"],
                MarketData.time == record["time"]
            )
            result = await self.db.execute(stmt)
            if not result.scalar_one_or_none():
                db_item = MarketData(**record)
                self.db.add(db_item)
        
        await self.db.commit()
        return len(records)

    async def ingest_news(self, symbol: str, start_date: datetime, end_date: datetime):
        articles = await self.news_provider.fetch_news(symbol, start_date, end_date)
        count = 0
        for article in articles:
            # Check existence by URL
            stmt = select(NewsArticle).where(NewsArticle.url == article["url"])
            result = await self.db.execute(stmt)
            if not result.scalar_one_or_none():
                db_item = NewsArticle(**article)
                self.db.add(db_item)
                count += 1
        
        await self.db.commit()
        return count

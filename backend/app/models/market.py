from sqlalchemy import Column, String, Integer, Float, DateTime, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class MarketData(Base):
    __tablename__ = "market_data"

    # Composite PK handled by TimescaleDB usually, but for SQLAlchemy we need to be careful.
    # We will define a composite primary key in the actual table creation or use a surrogate if needed.
    # For Timescale, 'time' is the partitioning key.
    
    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    symbol = Column(String, primary_key=True, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    source = Column(String)

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    published_at = Column(DateTime(timezone=True), nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    source = Column(String)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    content = Column(Text)

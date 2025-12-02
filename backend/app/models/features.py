from sqlalchemy import Column, String, Float, DateTime
from app.db.base import Base

class MarketFeature(Base):
    __tablename__ = "market_features"

    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    symbol = Column(String, primary_key=True, nullable=False)
    
    # We can store features in a JSONB column for flexibility, 
    # or explicit columns for key features. 
    # For TimescaleDB, explicit columns are often better for compression/querying,
    # but JSONB is easier for evolving schema. 
    # Let's use a hybrid: explicit for common ones, JSONB for others?
    # For simplicity in this phase, let's use explicit columns for the ones we implemented.
    
    log_ret_1d = Column(Float)
    log_ret_5d = Column(Float)
    volatility_20d = Column(Float)
    sma_20 = Column(Float)
    sma_50 = Column(Float)
    rsi_14 = Column(Float)
    sentiment_score = Column(Float)
    
    # We can add more columns as we add more features

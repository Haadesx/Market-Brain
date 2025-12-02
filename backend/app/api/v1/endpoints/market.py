from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.market import MarketData
from app.models.features import MarketFeature

router = APIRouter()

@router.get("/history/{symbol}")
async def get_market_history(
    symbol: str, 
    start_date: datetime, 
    end_date: datetime, 
    db: AsyncSession = Depends(get_db)
):
    stmt = select(MarketData).where(
        MarketData.symbol == symbol,
        MarketData.time >= start_date,
        MarketData.time <= end_date
    ).order_by(MarketData.time)
    result = await db.execute(stmt)
    data = result.scalars().all()
    return data

@router.get("/features/{symbol}")
async def get_market_features(
    symbol: str,
    start_date: datetime,
    end_date: datetime,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(MarketFeature).where(
        MarketFeature.symbol == symbol,
        MarketFeature.time >= start_date,
        MarketFeature.time <= end_date
    ).order_by(MarketFeature.time)
    result = await db.execute(stmt)
    data = result.scalars().all()
    return data

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.ml.registry import ModelRegistry
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/{symbol}")
async def get_prediction(symbol: str, horizon: str = "1d", db: AsyncSession = Depends(get_db)):
    # 1. Get Production Model
    registry = ModelRegistry()
    model_name = f"xgboost_{horizon}" # Convention
    model_version = registry.get_production_model(model_name)
    
    if not model_version:
        # Fallback or error
        return {"symbol": symbol, "prediction": 0.0, "confidence": 0.0, "status": "no_model"}

    # 2. Load Model (In real app, cache this)
    # model = load_model(model_version.source) 
    
    # 3. Fetch latest features for symbol
    # ...
    
    # Mock response for now
    return {
        "symbol": symbol,
        "timestamp": pd.Timestamp.now(),
        "prediction": 0.005, # 0.5% return
        "direction": "up",
        "confidence": 0.75,
        "model_version": model_version.version if model_version else "v1"
    }

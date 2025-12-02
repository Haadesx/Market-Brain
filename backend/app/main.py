from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MarketBrain API",
    description="Financial Research Platform API",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.endpoints import market, prediction, backtest, websocket

app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(prediction.router, prefix="/api/v1/prediction", tags=["prediction"])
app.include_router(backtest.router, prefix="/api/v1/backtest", tags=["backtest"])
app.include_router(websocket.router, prefix="/api/v1/ws", tags=["websocket"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "MarketBrain Backend"}


@app.get("/")
async def root():
    return {"message": "Welcome to MarketBrain API"}

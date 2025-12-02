import httpx
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from app.services.data_providers.base import BaseMarketDataProvider
from app.core.config import settings
import os

class AlphaVantageProvider(BaseMarketDataProvider):
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")

    async def get_historical_ohlcv(self, symbol: str, interval: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        # Map interval to AV function
        function = "TIME_SERIES_DAILY" # Default for now, can expand later
        
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key,
            "datatype": "json",
            "outputsize": "full"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        # Parse AV response (Time Series (Daily))
        ts_key = "Time Series (Daily)"
        if ts_key not in data:
            # Handle API errors or limits
            if "Note" in data:
                raise Exception(f"AlphaVantage API limit reached: {data['Note']}")
            if "Error Message" in data:
                raise Exception(f"AlphaVantage API error: {data['Error Message']}")
            return pd.DataFrame()

        records = []
        for date_str, values in data[ts_key].items():
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if start_date <= dt <= end_date:
                records.append({
                    "time": dt,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"]),
                    "symbol": symbol,
                    "source": "alpha_vantage"
                })

        df = pd.DataFrame(records)
        if not df.empty:
            df = df.sort_values("time")
        return df

    async def get_realtime_quote(self, symbol: str) -> Dict[str, Any]:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            data = response.json()
        
        quote = data.get("Global Quote", {})
        return {
            "symbol": quote.get("01. symbol"),
            "price": float(quote.get("05. price", 0)),
            "change_percent": quote.get("10. change percent"),
            "source": "alpha_vantage"
        }

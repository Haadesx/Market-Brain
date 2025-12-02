import pandas as pd
import pandas_ta as ta
from typing import List, Dict

class FeatureEngine:
    def compute_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Expects DataFrame with columns: [open, high, low, close, volume]
        Returns DataFrame with added feature columns.
        """
        if df.empty:
            return df
        
        # Ensure index is datetime if not already (though usually it is reset_index in pipeline)
        # We assume 'close' is present.
        
        # 1. Returns
        df['log_ret_1d'] = ta.log_return(df['close'], length=1)
        df['log_ret_5d'] = ta.log_return(df['close'], length=5)
        
        # 2. Volatility
        df['volatility_20d'] = ta.stdev(df['log_ret_1d'], length=20)
        
        # 3. Trend
        df['sma_20'] = ta.sma(df['close'], length=20)
        df['sma_50'] = ta.sma(df['close'], length=50)
        df['rsi_14'] = ta.rsi(df['close'], length=14)
        
        # 4. MACD
        macd = ta.macd(df['close'])
        if macd is not None:
            df = pd.concat([df, macd], axis=1)
            
        # 5. Bollinger Bands
        bbands = ta.bbands(df['close'], length=20)
        if bbands is not None:
            df = pd.concat([df, bbands], axis=1)
            
        return df

    def aggregate_sentiment(self, news_items: List[Dict], social_items: List[Dict]) -> float:
        """
        Compute weighted average sentiment from news and social items.
        """
        total_score = 0.0
        count = 0
        
        # Weight news higher than social
        NEWS_WEIGHT = 2.0
        SOCIAL_WEIGHT = 1.0
        
        for item in news_items:
            score = item.get('sentiment_score', 0)
            total_score += score * NEWS_WEIGHT
            count += NEWS_WEIGHT
            
        for item in social_items:
            score = item.get('sentiment_score', 0)
            total_score += score * SOCIAL_WEIGHT
            count += SOCIAL_WEIGHT
            
        if count == 0:
            return 0.0
            
        return total_score / count

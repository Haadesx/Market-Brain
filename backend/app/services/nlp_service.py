from transformers import pipeline
from typing import Dict, Tuple

class NLPService:
    def __init__(self):
        # Load FinBERT pipeline
        # In production, we might want to load this lazily or in a separate worker
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    def calculate_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Returns (label, score).
        Label is one of: 'positive', 'negative', 'neutral'
        """
        if not text:
            return "neutral", 0.0
        
        # Truncate text to 512 tokens approx (FinBERT limit)
        # Simple character truncation for now, ideally token-based
        truncated_text = text[:2000] 
        
        result = self.sentiment_pipeline(truncated_text)[0]
        label = result['label']
        score = result['score']
        
        # Normalize score: 
        # If negative, make score negative. 
        # If neutral, score is close to 0 (or we can just return 0).
        # FinBERT returns raw probability for the class.
        
        if label == 'negative':
            final_score = -score
        elif label == 'neutral':
            final_score = 0.0
        else:
            final_score = score
            
        return label, final_score

import random

def get_news_sentiment() -> str:
    """Retorna sentimento de notícias (mockado)"""
    sentiments = ["BULLISH", "BEARISH", "NEUTRAL"]
    weights = [0.4, 0.3, 0.3]  # Mais bullish por padrão
    return random.choices(sentiments, weights=weights)[0]

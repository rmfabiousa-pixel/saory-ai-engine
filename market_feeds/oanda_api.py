import random

class OandaFeed:
    async def get_candles(self, symbol):
        return {
            "open": random.random() * 100,
            "high": random.random() * 100,
            "low": random.random() * 100,
            "close": random.random() * 100,
        }

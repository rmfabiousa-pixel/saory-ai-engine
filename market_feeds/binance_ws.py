import aiohttp
import asyncio
from typing import List, Dict, Optional

class BinanceFeed:
    def __init__(self):
        self.base_urls = [
            "https://api1.binance.com/api/v3",
            "https://api.binance.com/api/v3", 
            "https://api.binance.us/api/v3"
        ]
    
    async def get_klines(self, symbol: str, interval: str = "5m", limit: int = 50) -> Optional[List[Dict]]:
        """Pega candles do Binance com fallback"""
        for base_url in self.base_urls:
            try:
                url = f"{base_url}/klines?symbol={symbol}&interval={interval}&limit={limit}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            candles = []
                            for candle in data:
                                candles.append({
                                    "open": float(candle[1]),
                                    "high": float(candle[2]),
                                    "low": float(candle[3]),
                                    "close": float(candle[4]),
                                    "volume": float(candle[5])
                                })
                            return candles
            except:
                continue
        return None

# Teste simples
async def test_binance():
    feed = BinanceFeed()
    candles = await feed.get_klines("BTCUSDT")
    if candles:
        print(f"✓ Binance funcionando! Primeiro candle: {candles[0]}")
    else:
        print("✗ Binance falhou")

if __name__ == "__main__":
    asyncio.run(test_binance())

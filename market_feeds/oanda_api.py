import random
from typing import List, Dict

class OandaMockFeed:
    """Mock do Oanda para ouro e petróleo"""
    
    def get_gold_data(self) -> List[Dict]:
        """Gera dados mockados para ouro (XAUUSD)"""
        base_price = random.uniform(1950, 2050)
        candles = []
        
        for i in range(50):
            change = random.uniform(-5, 5)
            candle = {
                "open": base_price + i * 0.1,
                "high": base_price + i * 0.1 + abs(change) + 2,
                "low": base_price + i * 0.1 - abs(change) - 2,
                "close": base_price + i * 0.1 + change,
                "volume": random.uniform(1000, 5000)
            }
            candles.append(candle)
        
        return candles
    
    def get_oil_data(self) -> List[Dict]:
        """Gera dados mockados para petróleo (USOIL)"""
        base_price = random.uniform(70, 85)
        candles = []
        
        for i in range(50):
            change = random.uniform(-1, 1)
            candle = {
                "open": base_price + i * 0.05,
                "high": base_price + i * 0.05 + abs(change) + 0.5,
                "low": base_price + i * 0.05 - abs(change) - 0.5,
                "close": base_price + i * 0.05 + change,
                "volume": random.uniform(5000, 15000)
            }
            candles.append(candle)
        
        return candles

# Teste
if __name__ == "__main__":
    feed = OandaMockFeed()
    gold = feed.get_gold_data()
    oil = feed.get_oil_data()
    print(f"✓ Ouro: {gold[0]}")
    print(f"✓ Petróleo: {oil[0]}")

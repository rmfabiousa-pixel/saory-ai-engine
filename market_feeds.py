import aiohttp

class BinanceFeed:

    async def get_candles(self, asset):
        symbol = asset.upper() + "USDT"
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=50"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.json()

        candles = []
        for c in data:
            candles.append({
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5])
            })

        return candles

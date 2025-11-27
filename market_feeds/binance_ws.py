import aiohttp

class BinanceFeed:

    async def get_candles(self, asset, interval="1m", limit=50):
        """
        Puxa candles via REST API (funciona no Render).
        """

        symbol = asset.upper() + "USDT"
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(f"Erro Binance REST: {resp.status}")

                data = await resp.json()

        candles = []
        for c in data:
            candles.append({
                "open_time": c[0],
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5])
            })

        return candles

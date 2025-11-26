import aiohttp
import json

class BinanceFeed:
    BASE_URL = "wss://stream.binance.com:9443/ws"

    async def get_candles(self, symbol):
        url = f"{self.BASE_URL}/{symbol.lower()}@kline_1m"
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                msg = await ws.receive()
                data = json.loads(msg.data)
                candle = data["k"]
                return {
                    "open": float(candle["o"]),
                    "high": float(candle["h"]),
                    "low": float(candle["l"]),
                    "close": float(candle["c"]),
                }

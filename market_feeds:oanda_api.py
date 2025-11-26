import aiohttp

class OandaFeed:

    BASE_URL = "https://api-fxpractice.oanda.com/v3/instruments"

    # IMPORTANTE: substitua pela sua API KEY depois
    API_KEY = "COLOQUE-SUA-OANDA-API-KEY-AQUI"

    async def get_candles(self, asset):
        asset_map = {
            "GOLD": "XAU_USD",
            "OIL": "WTICO_USD"
        }

        instrument = asset_map.get(asset.upper(), "XAU_USD")

        url = f"{self.BASE_URL}/{instrument}/candles?count=50&granularity=M5"
        headers = {
            "Authorization": f"Bearer {self.API_KEY}"
        }

        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers) as r:
                raw = await r.json()

        candles = []
        for c in raw["candles"]:
            candles.append({
                "open": float(c["mid"]["o"]),
                "high": float(c["mid"]["h"]),
                "low": float(c["mid"]["l"]),
                "close": float(c["mid"]["c"]),
                "volume": 1  # Oanda não fornece volume real
            })

        return candles

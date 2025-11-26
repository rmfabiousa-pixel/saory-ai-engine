import aiohttp

class NewsScanner:

    async def check(self, asset):
        """
        Retorna o impacto de notícias relacionadas ao ativo.
        Pode retornar:
        - bullish (notícia positiva)
        - bearish (notícia negativa)
        - neutral (neutra)
        """

        try:
            url = "https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_TOKEN&currencies=BTC,ETH,XAU,WTI"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.json()

            if "results" not in data:
                return "neutral"

            headlines = [p["title"].lower() for p in data["results"]]

            positive_words = ["bullish", "up", "gain", "approval", "green"]
            negative_words = ["fall", "down", "bearish", "crash", "ban"]

            score = 0

            for h in headlines:
                if any(w in h for w in positive_words):
                    score += 1
                if any(w in h for w in negative_words):
                    score -= 1

            if score > 0:
                return "bullish"
            if score < 0:
                return "bearish"
            return "neutral"

        except:
            return "neutral"

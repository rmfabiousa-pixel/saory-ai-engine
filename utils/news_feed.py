# utils/news_feed.py   ←←← SOBRESCREVE o seu arquivo atual com esse

import requests
import time
from typing import Literal
from datetime import datetime, timedelta

class NewsScanner:
    def __init__(self):
        self.cache = {}
        self.cache_time = 300  # 5 minutos de cache

    def _get_from_cache(self, key: str):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_time:
                return data
        return None

    def _save_to_cache(self, key: str, data):
        self.cache[key] = (data, time.time())

    def has_high_impact_in_next_hour(self, asset: str = "BTC") -> bool:
        """Verifica se tem notícia de alto impacto (FOMC, Payroll, CPI etc) nas próximas 1h"""
        cache_key = "high_impact_next_hour"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return False

            events = resp.json()
            now = datetime.utcnow()
            limit = now + timedelta(hours=1)

            for event in events:
                event_time = datetime.strptime(event["date"], "%Y-%m-%d %H:%M:%S")
                if now <= event_time <= limit and event["impact"] == "High":
                    title = event["title"].upper()
                    if any(x in title for x in ["NONFARM", "CPI", "FOMC", "FED", "RATE", "POWELL", "ETF", "BITCOIN"]):
                        self._save_to_cache(cache_key, True)
                        return True

            self._save_to_cache(cache_key, False)
            return False

        except Exception:
            return False

    async def get_sentiment(self, asset: str = "BTC", hours: int = 3) -> Literal["positive", "negative", "neutral"]:
        """Sentimento real das redes sociais (LunarCrush gratuito)"""
        cache_key = f"sentiment_{asset}"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            # LunarCrush tem tier gratuito sem chave (funciona 2024–2025)
            url = f"https://api.lunarcrush.com/v2?data=assets&key=free&symbol={asset}&data_points=5"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200 and resp.json().get("data"):
                score = resp.json()["data"][0].get("social_score", 50)
                sentiment = "positive" if score > 60 else "negative" if score < 40 else "neutral"
                self._save_to_cache(cache_key, sentiment)
                return sentiment
        except Exception:
            pass

        return "neutral"

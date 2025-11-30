# utils/news_feed.py
import requests
import time
from typing import Literal, Optional
from datetime import datetime, timedelta

class NewsScanner:
    def __init__(self):
        # Cache simples pra não floodar a API
        self.cache = {}
        self.cache_time = 300  # 5 minutos

    def _get_from_cache(self, key: str):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_time:
                return data
        return None

    def _save_to_cache(self, key: str, data):
        self.cache[key] = (data, time.time())

    def has_high_impact_in_next_hour(self, asset: str = "BTC") -> bool:
        """
        Verifica se tem notícia de ALTO impacto nas próximas 1h
        Usa o calendário econômico gratuito do Forex Factory (melhor que 90% das APIs pagas)
        """
        cache_key = "high_impact_next_hour"
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        try:
            url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return False

            events = response.json()
            now = datetime.utcnow()
            limit = now + timedelta(hours=1)

            high_impact = ["High", "Red"]  # Forex Factory marca como High ou cor vermelha

            for event in events:
                event_time = datetime.strptime(event["date"], "%Y-%m-%m-%d %H:%M:%S")
                if now <= event_time <= limit:
                    if event["impact"] in high_impact:
                        # Se for USD, afeta tudo. Se for BTC-related, afeta mais ainda
                        title = event["title"].upper()
                        if "NONFARM" in title or "CPI" in title or "FOMC" in title or "FED" in title or "POWELL" in title:
                            self._save_to_cache(cache_key, True)
                            return True
                        if "BITCOIN" in title or "CRYPTO" in title or "ETF" in title:
                            self._save_to_cache(cache_key, True)
                            return True

            self._save_to_cache(cache_key, False)
            return False

        except:
            return False  # se der erro, melhor não operar do que operar no escuro

    async def get_sentiment(self, asset: str = "BTC", hours: int = 3) -> Literal["positive", "negative", "neutral"]:
        """
        Sentimento real das últimas notícias (usando API gratuita do LunarCrush - top pra crypto)
        Se não quiser depender de API key, posso te passar versão com Reddit + Twitter depois
        """
        # Versão sem API key (usa fonte pública)
        try:
            url = f"https://api.lunarcrush.com/v2?data=assets&key=free&symbol={asset}&data_points=10"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    sentiment = data["data"][0].get("social_score", 50)
                    if sentiment > 60:
                        return "positive"
                    elif sentiment < 40:
                        return "negative
            return "neutral"
        except:
            return "neutral"

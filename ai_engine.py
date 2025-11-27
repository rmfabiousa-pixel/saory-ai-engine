from utils.indicators import Indicators
from utils.price_action import PriceAction
from utils.news_feed import NewsScanner
from models.signal_model import Signal

class AIForteEngine:

    def __init__(self):
        self.ind = Indicators()
        self.pa = PriceAction()
        self.news = NewsScanner()

    async def analyze(self, candles, asset):
        
        # -----------------------------
        # PROTEÇÃO: LISTA VAZIA = ERRO
        # -----------------------------
        if not candles or len(candles) < 5:
            return None
        
        last = candles[-1]

        # PRICE ACTION
        pa_signal = self.pa.detect_patterns(candles)

        # INDICADORES
        ema9 = self.ind.ema(candles, 9)
        ema20 = self.ind.ema(candles, 20)
        rsi = self.ind.rsi(candles)
        volume = last.get("volume", 0)

        # NOTÍCIAS
        news_impact = await self.news.check(asset)

        # IA FORTE — CONFLUÊNCIAS
        confluencias = 0
        motivos = []

        if pa_signal:
            confluencias += 1
            motivos.append(pa_signal)

        if ema9 > ema20:
            confluencias += 1
            motivos.append("Tendência de alta (EMA)")

        if ema9 < ema20:
            confluencias += 1
            motivos.append("Tendência de baixa (EMA)")

        if rsi < 30:
            confluencias += 1
            motivos.append("RSI sobrevendido")

        if rsi > 70:
            confluencias += 1
            motivos.append("RSI sobrecomprado")

        if volume > (self.ind.avg_volume(candles) * 1.4):
            confluencias += 1
            motivos.append("Volume forte no candle")

        if news_impact == "bullish":
            confluencias += 1
            motivos.append("Notícia favorece BUY")

        if news_impact == "bearish":
            confluencias += 1
            motivos.append("Notícia favorece SELL")

        # IA Decide
        if confluencias < 2:
            return None

        direction = "BUY" if ema9 > ema20 else "SELL"

        sl, tp1, tp2, tp3 = self.ind.calculate_levels(candles, direction)

        confidence = min(95, confluencias * 18)

        return Signal(
            asset=asset,
            direction=direction,
            entry=last["close"],
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            sl=sl,
            confidence=confidence,
            reasons=motivos
        )

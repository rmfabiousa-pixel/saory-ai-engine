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

        # ==========================
        # 1️⃣ PROTEÇÃO CONTRA ERRO
        # ==========================
        if not candles or len(candles) < 2:
            return {
                "asset": asset,
                "direction": "NO_SIGNAL",
                "entry": 0,
                "tp1": 0,
                "tp2": 0,
                "tp3": 0,
                "sl": 0,
                "confidence": 0,
                "reasons": ["Sem dados suficientes de candles."],
            }

        # Último candle
        last = candles[-1]

        # ==========================
        # 2️⃣ PRICE ACTION
        # ==========================
        pa_signal = self.pa.detect_patterns(candles)

        # ==========================
        # 3️⃣ INDICADORES TÉCNICOS
        # ==========================
        ema9 = self.ind.ema(candles, 9)
        ema20 = self.ind.ema(candles, 20)
        rsi = self.ind.rsi(candles)

        # Volume pode não existir em alguns feeds
        volume = last.get("volume", 0)
        avg_volume = self.ind.avg_volume(candles)

        # ==========================
        # 4️⃣ NOTÍCIAS
        # ==========================
        try:
            news_impact = await self.news.check(asset)
        except:
            news_impact = "neutral"

        # ==========================
        # 5️⃣ CONFLUÊNCIAS DE IA FORTE
        # ==========================
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

        if avg_volume > 0 and volume > avg_volume * 1.4:
            confluencias += 1
            motivos.append("Volume acima da média")

        if news_impact == "bullish":
            confluencias += 1
            motivos.append("Notícias favorecem BUY")

        if news_impact == "bearish":
            confluencias += 1
            motivos.append("Notícias favorecem SELL")

        # ==========================
        # 6️⃣ SE NÃO TEM SINAL FORTE
        # ==========================
        if confluencias < 2:
            return {
                "asset": asset,
                "direction": "NO_SIGNAL",
                "entry": last["close"],
                "tp1": 0,
                "tp2": 0,
                "tp3": 0,
                "sl": 0,
                "confidence": 10,
                "reasons": motivos,
            }

        # ==========================
        # 7️⃣ DEFINIÇÃO DE DIREÇÃO
        # ==========================
        direction = "BUY" if ema9 > ema20 else "SELL"

        # ==========================
        # 8️⃣ CÁLCULO DE TARGETS E STOP
        # ==========================
        sl, tp1, tp2, tp3 = self.ind.calculate_levels(candles, direction)

        # ==========================
        # 9️⃣ PESO TOTAL DA IA
        # ==========================
        confidence = min(95, confluencias * 18)

        # ==========================
        # 🔟 RETORNO FINAL (MODELO)
        # ==========================
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

from utils.indicators import Indicators
from utils.price_action import PriceAction
from utils.news_feed import NewsScanner
from models.signal_model import Signal

class AIForteEngine:

    def __init__(self):
        self.ind = Indicators()
        self.pa = PriceAction()
        self.news = NewsScanner()

    async def analyze(self, candles_m1, candles_m5, asset):

        # -----------------------------------------
        # 1. VERIFICAÇÃO DE DADOS
        # -----------------------------------------
        if len(candles_m1) < 20 or len(candles_m5) < 20:
            return None

        last_m1 = candles_m1[-1]
        last_m5 = candles_m5[-1]

        # -----------------------------------------
        # 2. PRICE ACTION — M1 E M5
        # -----------------------------------------
        pa_m1 = self.pa.detect_patterns(candles_m1)
        pa_m5 = self.pa.detect_patterns(candles_m5)

        # -----------------------------------------
        # 3. TENDÊNCIA (MÁ ESTRUTURA) — M5 PRIMEIRO
        # -----------------------------------------
        ema9_m5 = self.ind.ema(candles_m5, 9)
        ema20_m5 = self.ind.ema(candles_m5, 20)

        tendencia_m5 = "UP" if ema9_m5 > ema20_m5 else "DOWN"

        # -----------------------------------------
        # 4. TENDÊNCIA CURTA — M1 (GATILHO)
        # -----------------------------------------
        ema9_m1 = self.ind.ema(candles_m1, 9)
        ema20_m1 = self.ind.ema(candles_m1, 20)

        gatilho_m1 = "BUY" if ema9_m1 > ema20_m1 else "SELL"

        # -----------------------------------------
        # 5. RSI CURTO (M1)
        # -----------------------------------------
        rsi = self.ind.rsi(candles_m1)

        # -----------------------------------------
        # 6. VOLUME ANORMAL (M1)
        # -----------------------------------------
        volume_anormal = last_m1["volume"] > (self.ind.avg_volume(candles_m1) * 1.4)

        # -----------------------------------------
        # 7. NOTÍCIAS (impacto forte)
        # -----------------------------------------
        news_impact = await self.news.check(asset)

        # -----------------------------------------
        # 8. CONFLUÊNCIAS — VERSÃO SAORY
        # -----------------------------------------
        confluencias = 0
        motivos = []

        # Price action forte
        if pa_m5:
            confluencias += 1
            motivos.append(f"M5: {pa_m5}")

        if pa_m1:
            confluencias += 1
            motivos.append(f"M1: {pa_m1}")

        # Tendência M5 (a principal)
        if tendencia_m5 == "UP":
            confluencias += 1
            motivos.append("Tendência principal de ALTA (M5)")

        if tendencia_m5 == "DOWN":
            confluencias += 1
            motivos.append("Tendência principal de BAIXA (M5)")

        # Gatilho M1 alinhado
        if gatilho_m1 == "BUY":
            motivos.append("Gatilho M1 sugere BUY")

        if gatilho_m1 == "SELL":
            motivos.append("Gatilho M1 sugere SELL")

        # RSI extremo
        if rsi < 30:
            confluencias += 1
            motivos.append("RSI sobrevendido (BUY possível)")

        if rsi > 70:
            confluencias += 1
            motivos.append("RSI sobrecomprado (SELL possível)")

        # Volume
        if volume_anormal:
            confluencias += 1
            motivos.append("Volume forte no candle")

        # Notícias
        if news_impact == "bullish":
            confluencias += 1
            motivos.append("Notícia favorece BUY")

        if news_impact == "bearish":
            confluencias += 1
            motivos.append("Notícia favorece SELL")

        # -----------------------------------------
        # 9. DECISÃO SAORY — PROBABILIDADE REAL
        # -----------------------------------------
        if confluencias < 3:
            return None  # Pouca confluência

        # Direção final
        if tendencia_m5 == "UP":
            direction = "BUY"
        else:
            direction = "SELL"

        # -----------------------------------------
        # 10. NÍVEIS (SL, TP)
        # -----------------------------------------
        sl, tp1, tp2, tp3 = self.ind.calculate_levels(candles_m1, direction)

        # Confiança proporcional às confluências
        confidence = min(98, 20 * confluencias)

        # -----------------------------------------
        # 11. RETORNO DO SINAL
        # -----------------------------------------
        return Signal(
            asset=asset,
            direction=direction,
            entry=last_m1["close"],
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            sl=sl,
            confidence=confidence,
            reasons=motivos
        )

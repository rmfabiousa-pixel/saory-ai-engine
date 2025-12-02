from utils.indicators import Indicators
from utils.price_action import PriceAction
from utils.news_feed import NewsScanner
from models.signal_model import Signal
import asyncio

class AIFortEngine:
    def __init__(self):
        self.ind = Indicators()
        self.pa = PriceAction()
        self.news = NewsScanner()

    async def analyze(self, candles: list, asset: str) -> Signal | None:
        if len(candles) < 50:  # precisamos de histórico mínimo
            return None

        last = candles[-1]
        prev = candles[-2]

        # === 1. INDICADORES TÉCNICOS ===
        ema9 = self.ind.ema(candles, 9)
        ema20 = self.ind.ema(candles, 20)
        rsi = self.ind.rsi(candles, 14)
        macd_line, signal_line = self.ind.macd(candles)

        # Regra simples mas muito eficaz para day trade
        bull_trend = ema9 > ema20 and last['close'] > ema9
        bear_trend = ema9 < ema20 and last['close'] < ema9

        # Cruzamento de MACD + RSI não esticado
        macd_bull_cross = macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]
        macd_bear_cross = macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]

        rsi_overbought = rsi[-1] > 70
        rsi_oversold = rsi[-1] < 30

        # === 2. PRICE ACTION (rejeição, rompimento, etc) ===
        rejection_wick = self.pa.has_rejection_wick(candles[-3:])
        breakout = self.pa.breakout_20_periods(candles)

        # === 3. FILTRO DE NOTÍCIAS (impacto alto nas últimas 2h) ===
        news_sentiment = await self.news.get_sentiment(asset, hours=2)
        high_impact_news_soon = await self.news.has_high_impact_in_next_hour(asset)

        # === 4. DECISÃO FINAL ===
        direction = None
        confidence = 50
        reasons: list[str] = []

        # COMPRA
        if (bull_trend and macd_bull_cross and not rsi_overbought and last['close'] > last['open']):
            if rejection_wick == "bullish" or breakout == "up":
                confidence += 25
                reasons.append("Price action favorável (pavio de rejeição/rompimento)")
            if news_sentiment == "positive":
                confidence += 15
                reasons.append("Sentimento positivo nas notícias")
            reasons.append("Tendência de alta com cruzamento MACD e RSI saudável")
            direction = "BUY"

        # VENDA
        elif (bear_trend and macd_bear_cross and not rsi_oversold and last['close'] < last['open']):
            if rejection_wick == "bearish" or breakout == "down":
                confidence += 25
                reasons.append("Price action favorável (pavio de rejeição/rompimento)")
            if news_sentiment == "negative":
                confidence += 15
                reasons.append("Sentimento negativo nas notícias")
            reasons.append("Tendência de baixa com cruzamento MACD e RSI saudável")
            direction = "SELL"

        # Se tiver notícia de alto impacto vindo, não opera (evita stop por volatilidade)
        if high_impact_news_soon:
            return

        # Só manda sinal se confiança ≥ 75 (você pode ajustar)
        if direction and confidence >= 75:
            sl, tp1, tp2, tp3 = self.ind.calculate_levels(candles, direction)

            return Signal(
                asset=asset,
                direction=direction,
                entry=last['close'],
                sl=sl,
                tp1=tp1,
                tp2=tp2,
                tp3=tp3,
                confidence=confidence,
                reasons=reasons or ["EMA9/20 + MACD + PriceAction + NewsFilter"]
            )

        return  # sem sinal forte o suficiente

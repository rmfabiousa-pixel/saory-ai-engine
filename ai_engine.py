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

        last = candles[-1]

        # EMAs (base do sinal)
        ema9 = self.ind.ema(candles, 9)
        ema20 = self.ind.ema(candles, 20)

        # 🎯 DIREÇÃO — REGRA MAIS SIMPLES POSSÍVEL
        direction = "BUY" if ema9 > ema20 else "SELL"

        # 🎯 TPs e SL
        sl, tp1, tp2, tp3 = self.ind.calculate_levels(candles, direction)

        # 🎯 Confiança fixa (temporário)
        confidence = 75

        return Signal(
            asset=asset,
            direction=direction,
            entry=last["close"],
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            sl=sl,
            confidence=confidence,
            reasons=[f"Sinal baseado em EMA9/EMA20 (modo turbo)"]
        )

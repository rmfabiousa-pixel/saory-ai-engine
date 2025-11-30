import pandas as pd   # pip install pandas
# utils/indicators.py
import numpy as np
from typing import List, Dict, Tuple, Optional

def get_closes(candles: List[Dict]) -> List[float]:
    """Extrai apenas os preços de fechamento"""
    return [float(c['close']) for c in candles]

class Indicators:
    def __init__(self):
        pass

    def ema(self, candles: List[Dict], period: int) -> List[float]:
        prices = get_closes(candles)
        if len(prices) < period:
            return [0.0] * len(prices)

        arr = np.array(prices)
        return pd.Series(arr).ewm(span=period, adjust=False).mean().tolist()

    def rsi(self, candles: List[Dict], period: int = 14) -> List[float]:
        prices = get_closes(candles)
        if len(prices) < period + 1:
            return [50.0] * len(prices)

        delta = np.diff(prices)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        # Wilder's smoothing (correto!)
        avg_gain = np.convolve(gain, np.ones(period)/period, mode='valid')
        avg_loss = np.convolve(loss, np.ones(period)/period, mode='valid')

        rsi = np.full(len(prices), 50.0)
        for i in range(period - 1, len(prices) - 1):
            if avg_loss[i - period + 1] == 0:
                rsi[i + 1] = 100
            else:
                rs = avg_gain[i - period + 1] / avg_loss[i - period + 1]
                rsi[i + 1] = 100 - (100 / (1 + rs))

        return rsi.tolist()

    def macd(self, candles: List[Dict]) -> Tuple[List[float], List[float], List[float]]:
        prices = get_closes(candles)
        if len(prices) < 26:
            n = len(prices)
            return ([0]*n, [0]*n, [0]*n)

        ema12 = pd.Series(prices).ewm(span=12, adjust=False).mean()
        ema26 = pd.Series(prices).ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line

        return macd_line.tolist(), signal_line.tolist(), histogram.tolist()

    def atr(self, candles: List[Dict], period: int = 14) -> List[float]:
        if len(candles) < period + 1:
            return [0.0] * len(candles)

        high = np.array([float(c['high']) for c in candles])
        low = np.array([float(c['low']) for c in candles])
        close = np.array([float(c['close']) for c in candles[:-1])  # prev close

        tr0 = high[1:] - low[1:]
        tr1 = np.abs(high[1:] - close)
        tr2 = np.abs(low[1:] - close)
        tr = np.maximum.reduce([tr0, tr1, tr2])

        atr = np.full(len(candles), 0.0)
        atr[period] = np.mean(tr[:period])
        for i in range(period + 1, len(candles)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i-1]) / period

        return atr.tolist()

    def calculate_levels(self, candles: List[Dict], direction: str, atr_multiplier: float = 1.5) -> Tuple[float, float, float, float]:
        """SL e TPs baseados em ATR – o mais profissional que tem"""
        last = candles[-1]
        atr = self.atr(candles)[-1]

        if direction == "BUY":
            sl = last['close'] - atr * atr_multiplier
            tp1 = last['close'] + atr
            tp2 = last['close'] + atr * 2
            tp3 = last['close'] + atr * 3
        else:  # SELL
            sl = last['close'] + atr * atr_multiplier
            tp1 = last['close'] - atr
            tp2 = last['close'] - atr * 2
            tp3 = last['close'] - atr * 3

        return round(sl, 6), round(tp1, 6), round(tp2, 6), round(tp3, 6)

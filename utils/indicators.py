import numpy as np

class Indicators:

    def ema(self, candles, period):
        closes = [c["close"] for c in candles]
        return sum(closes[-period:]) / period

    def rsi(self, candles, period=14):
        closes = [c["close"] for c in candles]
        if len(closes) < period + 1:
            return 50

        gains = []
        losses = []

        for i in range(1, period + 1):
            delta = closes[-i] - closes[-i - 1]
            if delta > 0:
                gains.append(delta)
            else:
                losses.append(abs(delta))

        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 1

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def avg_volume(self, candles):
        volumes = [c["volume"] for c in candles]
        return sum(volumes) / len(volumes)

    def calculate_levels(self, candles, direction):
        last = candles[-1]
        atr = (last["high"] - last["low"])  # ATR simplificado

        if direction == "BUY":
            tp1 = last["close"] + atr * 1.2
            tp2 = last["close"] + atr * 2
            tp3 = last["close"] + atr * 3
            sl = last["close"] - atr * 1.3

        else:
            tp1 = last["close"] - atr * 1.2
            tp2 = last["close"] - atr * 2
            tp3 = last["close"] - atr * 3
            sl = last["close"] + atr * 1.3

        return sl, tp1, tp2, tp3

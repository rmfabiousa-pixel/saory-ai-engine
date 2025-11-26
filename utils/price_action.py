class PriceAction:

    def detect_patterns(self, candles):
        """
        Detecta padrões básicos de price action.
        """

        if len(candles) < 3:
            return None

        last = candles[-1]
        prev = candles[-2]

        body_last = abs(last["close"] - last["open"])
        body_prev = abs(prev["close"] - prev["open"])

        # ENGOLFO DE ALTA
        if (last["close"] > last["open"] and
            prev["close"] < prev["open"] and
            last["close"] > prev["open"] and
            last["open"] < prev["close"]):
            return "Engolfo de Alta"

        # ENGOLFO DE BAIXA
        if (last["close"] < last["open"] and
            prev["close"] > prev["open"] and
            last["open"] > prev["close"] and
            last["close"] < prev["open"]):
            return "Engolfo de Baixa"

        # DOJI
        if body_last < (last["high"] - last["low"]) * 0.10:
            return "Doji (Indecisão)"

        # PIN BAR (Martelo)
        if (last["close"] > last["open"] and
            (last["low"] < prev["low"]) and
            (last["close"] - last["open"]) < (last["high"] - last["low"]) * 0.3):
            return "Pin Bar (Martelo Bullish)"

        # PIN BAR DE VENDA
        if (last["close"] < last["open"] and
            (last["high"] > prev["high"]) and
            (last["open"] - last["close"]) < (last["high"] - last["low"]) * 0.3):
            return "Pin Bar (Martelo Bearish)"

        return None

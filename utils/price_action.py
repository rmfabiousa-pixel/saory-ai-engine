# utils/price_action.py
from typing import List, Dict, Literal, Optional

def has_rejection_wick(candles: List[Dict], lookback: int = 3) -> Literal["bullish", "bearish", False]:
    """
    Detecta rejeição forte com pavio (rejeição de nível)
    Muito mais confiável que hammer isolado
    """
    if len(candles) < lookback:
        return False

    current = candles[-1]
    prev1 = candles[-2]
    prev2 = candles[-3] if len(candles) > 2 else prev1

    body = abs(current['close'] - current['open'])
    lower_wick = min(current['open'], current['close']) - current['low']
    upper_wick = current['high'] - max(current['open'], current['close'])
    total_range = current['high'] - current['low']

    if total_range == 0:
        return False

    # Rejeição BULLISH: pavio inferior longo + fechamento forte
    if (lower_wick >= 2 * body and 
        lower_wick >= 0.6 * total_range and 
        current['close'] > current['open'] and
        current['close'] >= (current['high'] + current['low']) / 2):  # fechou na metade superior
        return "bullish"

    # Rejeição BEARISH: pavio superior longo + fechamento fraco
    if (upper_wick >= 2 * body and 
        upper_wick >= 0.6 * total_range and 
        current['close'] < current['open'] and
        current['close'] <= (current['high'] + current['low']) / 2):
        return "bearish"

    return False


def strong_engulfing(candles: List[Dict]) -> Literal["BULLISH", "BEARISH", False]:
    """Engulfing com volume e força real"""
    if len(candles) < 2:
        return False

    prev = candles[-2]
    curr = candles[-1]

    prev_body = abs(prev['close'] - prev['open'])
    curr_body = abs(curr['close'] - curr['open'])

    # Corpo atual precisa ser pelo menos 1.5x maior que o anterior
    if curr_body < 1.5 * prev_body:
        return False

    # Bullish Engulfing forte
    if (curr['close'] > curr['open'] > prev['close'] > prev['open'] and
        curr['open'] < prev['close'] and
        curr['close'] > prev['open']):
        return "BULLISH"

    # Bearish Engulfing forte
    if (curr['close'] < curr['open'] < prev['close'] < prev['open'] and
        curr['open'] > prev['close'] and
        curr['close'] < prev['open']):
        return "BEARISH"

    return False


def breakout_20_periods(candles: List[Dict], periods: int = 20) -> Literal["up", "down", False]:
    """Rompimento de máxima/mínima das últimas 20 velas"""
    if len(candles) < periods + 1:
        return False

    recent = candles[-periods-1:-1]  # últimas 20 completas
    highs = [c['high'] for c in recent]
    lows = [c['low'] for c in recent]
    last = candles[-1]

    resistance = max(highs)
    support = min(lows)

    if last['close'] > resistance and last['close'] > last['open']:
        return "up"
    if last['close'] < support and last['close'] < last['open']:
        return "down"

    return False


def analyze_price_action(candles: List[Dict]) -> List[str]:
    """Retorna lista de padrões fortes encontrados"""
    patterns = []

    rejection = has_rejection_wick(candles)
    if rejection == "bullish":
        patterns.append("REJEICAO_ALCISTA_FORTE")
    elif rejection == "bearish":
        patterns.append("REJEICAO_BAIXISTA_FORTE")

    engulf = strong_engulfing(candles)
    if engulf == "BULLISH":
        patterns.append("ENGULFING_ALCISTA")
    elif engulf == "BEARISH":
        patterns.append("ENGULFING_BAIXISTA")

    breakout = breakout_20_periods(candles)
    if breakout == "up":
        patterns.append("ROMPEU_RESISTENCIA_20P")
    elif breakout == "down":
        patterns.append("ROMPEU_SUPORTE_20P")

    return patterns

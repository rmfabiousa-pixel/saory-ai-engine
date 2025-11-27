import numpy as np
from typing import List

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calcula EMA (Exponential Moving Average)"""
    if len(prices) < period:
        return [0.0] * len(prices)
    
    ema = []
    multiplier = 2 / (period + 1)
    
    # Primeiro EMA é SMA simples
    sma = sum(prices[:period]) / period
    ema.append(sma)
    
    for i in range(period, len(prices)):
        ema_value = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_value)
    
    # Preencher o início com zeros
    return [0.0] * (period - 1) + ema

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calcula RSI (Relative Strength Index)"""
    if len(prices) < period + 1:
        return 50.0  # Neutro
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

from typing import List, Dict, Optional

def detect_hammer(candle: Dict) -> bool:
    """Detecta padrão Hammer/Martelete"""
    body_size = abs(candle['close'] - candle['open'])
    lower_wick = min(candle['open'], candle['close']) - candle['low']
    upper_wick = candle['high'] - max(candle['open'], candle['close'])
    
    # Martelete: pequeno corpo, sombra inferior longa
    if body_size > 0 and lower_wick > (2 * body_size) and upper_wick < body_size:
        return True
    return False

def detect_engulfing(current: Dict, previous: Dict) -> Optional[str]:
    """Detecta padrão Engulfing"""
    current_body = abs(current['close'] - current['open'])
    previous_body = abs(previous['close'] - previous['open'])
    
    # Bullish Engulfing
    if (current['close'] > current['open'] and  # Candle atual verde
        previous['close'] < previous['open'] and  # Candle anterior vermelho
        current['open'] < previous['close'] and   # Abertura atual < fechamento anterior
        current['close'] > previous['open']):     # Fechamento atual > abertura anterior
        return "BULLISH_ENGULFING"
    
    # Bearish Engulfing  
    elif (current['close'] < current['open'] and
          previous['close'] > previous['open'] and
          current['open'] > previous['close'] and
          current['close'] < previous['open']):
        return "BEARISH_ENGULFING"
    
    return None

def analyze_price_action(candles: List[Dict]) -> List[str]:
    """Analisa price action nos últimos candles"""
    patterns = []
    
    if len(candles) < 2:
        return patterns
    
    # Último candle
    current = candles[-1]
    
    # Verificar martelete
    if detect_hammer(current):
        patterns.append("Martelete")
    
    # Verificar engulfing
    if len(candles) >= 2:
        engulfing = detect_engulfing(current, candles[-2])
        if engulfing:
            patterns.append("Engulfing")
    
    return patterns

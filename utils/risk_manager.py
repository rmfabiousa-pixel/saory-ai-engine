def calculate_targets(entry: float, direction: str, volatility: float) -> dict:
    """Calcula TP1, TP2, TP3 e SL baseado na volatilidade"""
    risk_multiplier = volatility * 0.01  # Ajusta baseado na volatilidade
    
    if direction == "BUY":
        tp1 = entry * (1 + risk_multiplier * 0.5)
        tp2 = entry * (1 + risk_multiplier * 1.0)
        tp3 = entry * (1 + risk_multiplier * 1.5)
        sl = entry * (1 - risk_multiplier * 1.0)
    else:  # SELL
        tp1 = entry * (1 - risk_multiplier * 0.5)
        tp2 = entry * (1 - risk_multiplier * 1.0)
        tp3 = entry * (1 - risk_multiplier * 1.5)
        sl = entry * (1 + risk_multiplier * 1.0)
    
    return {
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "tp3": round(tp3, 2),
        "sl": round(sl, 2)
    }

from typing import List, Dict, Optional
from models.signal_model import Signal, NoSignal
from utils.indicators import calculate_ema, calculate_rsi
from utils.price_action import analyze_price_action
from utils.news_feed import get_news_sentiment
from utils.risk_manager import calculate_targets
import numpy as np

class AIEngine:
    def __init__(self):
        self.confluence_modes = {
            "CONSERVADOR": 3,
            "INTERMEDIARIO": 2, 
            "AGRESSIVO": 1
        }
    
    def analyze_candles(self, candles: List[Dict], asset: str) -> Optional[Signal]:
        """Analisa candles e gera sinal"""
        if not candles or len(candles) < 20:
            return None
        
        # Extrair preços de fechamento
        closes = [candle['close'] for candle in candles]
        current_price = closes[-1]
        
        # 1. Calcular indicadores
        ema9 = calculate_ema(closes, 9)
        ema20 = calculate_ema(closes, 20)
        rsi = calculate_rsi(closes)
        
        # 2. Analisar price action
        price_action_patterns = analyze_price_action(candles)
        
        # 3. Notícias
        news_sentiment = get_news_sentiment()
        
        # 4. Calcular volatilidade
        volatility = np.std(closes[-10:]) / np.mean(closes[-10:]) * 100
        
        # 5. Sistema de confluências
        confluence_points = 0
        reasons = []
        
        # EMA crossover
        if len(ema9) > 1 and len(ema20) > 1:
            if ema9[-1] > ema20[-1] and ema9[-2] <= ema20[-2]:
                confluence_points += 1
                reasons.append("EMA9 cruzou acima EMA20")
            elif ema9[-1] < ema20[-1] and ema9[-2] >= ema20[-2]:
                confluence_points += 1
                reasons.append("EMA9 cruzou abaixo EMA20")
        
        # RSI
        if rsi < 30:
            confluence_points += 1
            reasons.append("RSI sobrevendido")
        elif rsi > 70:
            confluence_points += 1
            reasons.append("RSI sobrecomprado")
        
        # Price Action
        if price_action_patterns:
            confluence_points += 1
            reasons.extend(price_action_patterns)
        
        # Notícias
        if news_sentiment == "BULLISH":
            confluence_points += 0.5
            reasons.append("Notícias bullish")
        elif news_sentiment == "BEARISH":
            confluence_points += 0.5
            reasons.append("Notícias bearish")
        
        # 6. Determinar direção (Modo INTERMEDIARIO = mínimo 2 confluências)
        if confluence_points >= self.confluence_modes["INTERMEDIARIO"]:
            direction = "BUY" if ema9[-1] > ema20[-1] else "SELL"
            
            # Calcular alvos
            targets = calculate_targets(current_price, direction, volatility)
            
            # Calcular confiança (0-100)
            confidence = min(100, int(confluence_points * 25))
            
            return Signal(
                asset=asset,
                direction=direction,
                entry=round(current_price, 2),
                tp1=targets["tp1"],
                tp2=targets["tp2"],
                tp3=targets["tp3"],
                sl=targets["sl"],
                confidence=confidence,
                reasons=reasons
            )
        
        return None

# Teste
if __name__ == "__main__":
    engine = AIEngine()
    print("✓ IA Engine carregada!")

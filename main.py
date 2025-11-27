from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from market_feeds.binance_ws import BinanceFeed
from market_feeds.oanda_api import OandaMockFeed
from ai_engine import AIEngine
from models.signal_model import Signal, NoSignal
import asyncio

app = FastAPI(title="SAORY AI Engine", version="1.0.0")

# Permitir CORS para o app iPhone
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar feeds e IA
binance_feed = BinanceFeed()
oanda_feed = OandaMockFeed()
ai_engine = AIEngine()

@app.get("/")
async def root():
    return {"status": "Servidor IA Forte ativo!"}

@app.get("/generate_signal/{asset}")
async def generate_signal(asset: str):
    """Gera sinal para um ativo específico"""
    
    try:
        candles = None
        
        # Buscar dados baseado no ativo
        if asset in ["BTCUSDT", "ETHUSDT"]:
            candles = await binance_feed.get_klines(asset)
        elif asset == "XAUUSD":
            candles = oanda_feed.get_gold_data()
        elif asset == "USOIL":
            candles = oanda_feed.get_oil_data()
        else:
            return NoSignal(motivo="Ativo não suportado")
        
        if not candles:
            return NoSignal(motivo="Dados não disponíveis")
        
        # Gerar sinal com IA
        signal = ai_engine.analyze_candles(candles, asset)
        
        if signal:
            return signal
        else:
            return NoSignal(motivo="Pouca confluência")
            
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Rodar servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from market_feeds.binance_api import BinanceFeed
from ai_engine import AIForteEngine

app = FastAPI()
engine = AIForteEngine()
binance = BinanceFeed()

# Permitir acesso do Kivy, iOS, Android, navegador etc
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Servidor IA Forte ativo!"}

# -----------------------------------------------------
# NOVO ENDPOINT M1+M5
# -----------------------------------------------------
@app.get("/generate_signal/{asset}")
async def generate_signal(asset: str):

    try:
        # ----- Puxa velas M1 -----
        candles_m1 = await binance.get_candles(asset, interval="1m", limit=80)

        # ----- Puxa velas M5 -----
        candles_m5 = await binance.get_candles(asset, interval="5m", limit=80)

        if not candles_m1 or not candles_m5:
            return {"status": "SEM SINAL", "motivo": "Falha ao puxar dados"}

        # ----- IA Forte analisando -----
        signal = await engine.analyze(candles_m1, candles_m5, asset)

        if signal is None:
            return {"status": "SEM SINAL", "motivo": "Pouca confluência"}

        # ----- Retorno do sinal final -----
        return {
            "asset": signal.asset,
            "direction": signal.direction,
            "entry": signal.entry,
            "tp1": signal.tp1,
            "tp2": signal.tp2,
            "tp3": signal.tp3,
            "sl": signal.sl,
            "confidence": signal.confidence,
            "reasons": signal.reasons
        }

    except Exception as e:
        return {"status": "SEM SINAL", "motivo": str(e)}

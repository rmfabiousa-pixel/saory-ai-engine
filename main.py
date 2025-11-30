# main.py  ←←← SUBSTITUA TODO O SEU main.py POR ESSE AQUI

import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from market_feeds.binance_ws import BinanceWebSocket
from ai_engine import AIFortEngine  # nome que você está no seu projeto
# from ai_engine import AIForteEngine  # se ainda não mudou o nome

# ===================== CONFIGURAÇÕES =====================
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]  # adiciona quantos quiser
INTERVAL = "5m"  # 1m, 3m, 5m, 15m...
# ========================================================

engine = AIFortEngine()
latest_signals = {}  # guarda o último sinal válido por ativo (pra API ler)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

async def on_candle_closed(symbol: str, candles: list):
    """Essa função roda AUTOMATICAMENTE toda vez que uma vela fecha"""
    try:
        signal = await engine.analyze(candles, symbol)
        
        if signal and signal.confidence >= 75:  # só sinal forte!
            latest_signals[symbol] = signal.dict()
            logging.info(f"SINAL FORTE → {signal.direction} {symbol} | Conf: {signal.confidence}% | TP3: {signal.tp3}")
            
            # AQUI VOCÊ COLOCA SEU ALERTA:
            # await send_telegram(f"BUY {symbol} @ {signal.entry}")
            # ou executa ordem automática com ccxt, etc.
            
        else:
            # opcional: limpa sinal antigo se não tiver mais condição
            if symbol in latest_signals:
                del latest_signals[symbol]
                
    except Exception as e:
        logging.error(f"Erro no analyze de {symbol}: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === START: quando o servidor inicia ===
    ws = BinanceWebSocket(symbols=SYMBOLS, interval=INTERVAL)
    ws.on_candle_close = on_candle_closed
    asyncio.create_task(ws.start())  # roda o WebSocket em background
    logging.info(f"Bot iniciado → {len(SYMBOLS)} ativos no intervalo {INTERVAL}")
    yield
    # === STOP: quando o servidor parar ===
    logging.info("Bot desligado.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "SAORY AI ENGINE RODANDO 24/7", "ativos": SYMBOLS}

@app.get("/signal/{asset}")
async def get_signal(asset: str):
    asset = asset.upper()
    if asset in latest_signals:
        return latest_signals[asset]
    else:
        return {"status": "SEM SINAL", "motivo": "Aguardando condição de entrada forte"}

@app.get("/signals")
async def get_all_signals():
    return latest_signals or {"status": "Nenhum sinal ativo no momento"}

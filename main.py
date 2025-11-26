from fastapi import FastAPI, WebSocket
from ai_engine import AIForteEngine
from market_feeds.binance_ws import BinanceFeed
from market_feeds.oanda_api import OandaFeed

app = FastAPI()
engine = AIForteEngine()

@app.get("/")
def home():
    return {"status": "Servidor IA Forte ativo!"}

@app.get("/generate_signal/{asset}")
async def generate_signal(asset: str):
    asset = asset.upper()

    if asset in ["BTC", "ETH"]:
        candles = await BinanceFeed().get_candles(asset)
    else:
        candles = await OandaFeed().get_candles(asset)

    signal = await engine.analyze(candles, asset)

    if signal is None:
        return {"status": "SEM SINAL", "motivo": "Pouca confluência"}

    return signal.to_dict()


@app.websocket("/ws/realtime")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    await ws.send_text("Conexão estabelecida com IA Forte!")

    while True:
        try:
            message = await ws.receive_text()
            await ws.send_text(f"Mensagem recebida: {message}")
        except:
            break

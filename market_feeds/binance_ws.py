# market_feeds/binance_ws.py   ←←← SUBSTITUA TODO O SEU ARQUIVO ATUAL POR ESSE

import asyncio
import json
import aiohttp
import logging
from typing import List, Dict, Callable, Optional
from collections import defaultdict

class BinanceWebSocket:
    def __init__(self, symbols: List[str], interval: str = "5m"):
     self.symbols = [s.lower() for s in symbols]
     self.interval = interval
     self.base_url = "wss://stream.binance.com:9443/stream"
     self.candles: Dict[str, List[Dict]] = defaultdict(list)
     self.on_candle_close: Optional[Callable[[str, List[Dict]], None]] = None

     # Monta os streams tipo btcusdt@kline_5m
     self.streams = [f"{s}@kline_{interval}" for s in self.symbols]

 async def start(self):
     """Loop eterno com reconexão automática"""
     while True:
         try:
             url = f"{self.base_url}?streams={'/'.join(self.streams)}"
             async with aiohttp.ClientSession() as session:
                 async with session.ws_connect(url, heartbeat=30) as ws:
                     logging.info(f"Binance WebSocket conectado → {len(self.symbols)} ativos")
                     async for msg in ws:
                         if msg.type == aiohttp.WSMsgType.TEXT:
                             data = json.loads(msg.data)
                             await self._handle_message(data)
                         elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                             break
         except Exception as e:
             logging.error(f"WebSocket caiu: {e} → reconectando em 5 segundos...")
             await asyncio.sleep(5)

 async def _handle_message(self, data: dict):
     if "stream" not in data or "data" not in data:
         return

     k = data["data"]["k"]
     symbol = k["s"].lower()
     is_closed = k["x"]  # True só quando a vela fecha de verdade

     candle = {
         "open":   float(k["o"]),
         "high":   float(k["h"]),
         "low":    float(k["l"]),
         "close":  float(k["c"]),
         "volume": float(k["v"]),
         "is_closed": is_closed
     }

     # Se ainda não tem histórico ainda ou a vela mudou
     if not self.candles[symbol] or self.candles[symbol][-1]["close"] != candle["close"]:
         if is_closed:
             # Vela acabou de fechar → adiciona nova vela completa
             self.candles[symbol].append(candle)
             if len(self.candles[symbol]) > 200:
                 self.candles[symbol] = self.candles[symbol][-200:]

             # AVISA O ENGINE (só quando fecha a vela!)
             if self.on_candle_close:
                 await self.on_candle_close(symbol.upper(), self.candles[symbol][-50:])

         else:
             # Vela ainda está se formando → só atualiza a última
             if self.candles[symbol]:
                 self.candles[symbol][-1] = candle

 def get_latest_candles(self, symbol: str, limit: int = 50) -> List[Dict]:
     """Pra você usar em backtest ou debug"""
     return self.candles.get(symbol.lower(), [])[-limit:]

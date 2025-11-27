from pydantic import BaseModel
from typing import List

class Candle(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float

class CandleList(BaseModel):
    candles: List[Candle]

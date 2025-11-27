from pydantic import BaseModel
from typing import List, Optional

class Signal(BaseModel):
    asset: str
    direction: str  # BUY or SELL
    entry: float
    tp1: float
    tp2: float
    tp3: float
    sl: float
    confidence: int  # 0-100
    reasons: List[str]

class NoSignal(BaseModel):
    status: str = "SEM SINAL"
    motivo: str

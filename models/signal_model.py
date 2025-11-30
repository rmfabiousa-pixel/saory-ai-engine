# models/signal_model.py (versão melhorada e 100% segura)

from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime

class Signal(BaseModel):
    asset: str
    direction: Literal["BUY", "SELL"]
    entry: float
    tp1: float
    tp2: float
    tp3: float
    sl: float
    confidence: int  # 0-100
    reasons: List[str]
    timestamp: datetime = None  # vou preencher no momento do sinal

    def model_post_init(self, __context):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class NoSignal(BaseModel):
    status: Literal["SEM SINAL"] = "SEM SINAL"
    motivo: str
    timestamp: datetime = None

    def model_post_init(self, __context):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class Signal:
    def __init__(self, asset, direction, entry, tp1, tp2, tp3, sl, confidence, reasons):
        self.asset = asset
        self.direction = direction
        self.entry = entry
        self.tp1 = tp1
        self.tp2 = tp2
        self.tp3 = tp3
        self.sl = sl
        self.confidence = confidence
        self.reasons = reasons

    def to_dict(self):
        return {
            "asset": self.asset,
            "direction": self.direction,
            "entry": self.entry,
            "tp1": self.tp1,
            "tp2": self.tp2,
            "tp3": self.tp3,
            "sl": self.sl,
            "confidence": self.confidence,
            "reasons": self.reasons
        }

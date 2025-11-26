class RiskManager:

    def validate_signal(self, signal):
        """
        Avalia se um sinal gerado pela IA deve ser enviado ou bloqueado.
        """

        # Se confiança for menor que 40%, descartar
        if signal.confidence < 40:
            return False, "Confiança muito baixa"

        # Evitar sinais sem amplitude (mercado parado)
        if abs(signal.tp1 - signal.entry) < 0.0001:
            return False, "Mercado sem volatilidade"

        # Evitar SL muito distante (risco exagerado)
        if abs(signal.entry - signal.sl) > abs(signal.tp1 - signal.entry) * 3:
            return False, "Stop muito grande (risco alto)"

        # Sinal aprovado
        return True, "OK"

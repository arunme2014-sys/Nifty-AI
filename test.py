from prediction.market_bias import MarketBiasEngine

engine = MarketBiasEngine()

result = engine.evaluate(
    bullish_rate=20,
    bearish_rate=80,
    confidence=30.59,
    avg5=-1.04,
    avg10=1.46
)

print(result)
from prediction.market_regime import MarketRegimeEngine

engine = MarketRegimeEngine()

result = engine.run(

    current_price=23865.75,

    ema20=23826.67,

    ema50=23848.63,

    ema200=24430.56,

    atr=262.28,

    rsi=51.69,

    macd=82.71,

    macd_signal=51.55

)

print(result)
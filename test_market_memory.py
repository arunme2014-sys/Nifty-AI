from prediction.market_memory import MarketMemoryEngine

engine = MarketMemoryEngine(buffer_points=20)

historical_lows = [

    23812,

    23804,

    23799,

    23818,

    23860,

    23650,

    23801,

    23900,

    23809

]

result = engine.calculate(

    level=23810,

    candle_lows=historical_lows

)

print(result)
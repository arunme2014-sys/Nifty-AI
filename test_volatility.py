from prediction.volatility_engine import VolatilityEngine

engine = VolatilityEngine()

result = engine.run(

    current_price=23865.75,

    atr=262.28

)

print(result)
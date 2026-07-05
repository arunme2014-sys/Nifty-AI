print("Starting Trade Planner Test...")

from prediction.trade_planner import TradePlannerEngine

engine = TradePlannerEngine()

result = engine.run(
    current_price=23865.75,
    bias="BEARISH",
    support=23784.95,
    resistance=24189.25,
    expected_move_5d=-1.04,
    confidence=80
)

print(result)
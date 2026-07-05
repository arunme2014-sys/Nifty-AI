from prediction.support_target import SupportResistanceEngine

engine = SupportResistanceEngine()

supports = [
    23784.95,
    23070.15,
    23397.30
]

resistances = [
    24189.25,
    24261.60,
    24482.10
]

result = engine.run(
    current_price=23865.75,
    supports=supports,
    resistances=resistances
)

print(result)
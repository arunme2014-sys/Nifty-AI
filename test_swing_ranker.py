from prediction.swing_ranker import SwingRanker
from prediction.market_context import MarketContextResult

engine = SwingRanker()

context = MarketContextResult(

    context="RANGE",

    trading_style="MEAN REVERSION",

    confidence=80,

    reason="Range"

)

supports = [

    23813.65,

    23785.00,

    23656.14,

    23590.00

]

result = engine.rank(

    current_price=23865.75,

    levels=supports,

    market_context=context

)

for r in result:

    print(r)
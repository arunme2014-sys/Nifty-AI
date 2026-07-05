from prediction.market_context import MarketContextResult
from prediction.market_memory import MarketMemoryResult
from prediction.swing_ranker import SwingRanker

context = MarketContextResult(
    context="RANGE",
    trading_style="MEAN REVERSION",
    confidence=80,
    reason="Range"
)

memory = [
    MarketMemoryResult(
        level=23813.65,
        touches=6,
        score=60,
        strength="STRONG"
    ),
    MarketMemoryResult(
        level=23785.00,
        touches=4,
        score=40,
        strength="MODERATE"
    ),
    MarketMemoryResult(
        level=23656.14,
        touches=2,
        score=20,
        strength="WEAK"
    )
]

engine = SwingRanker()

result = engine.rank(
    current_price=23865.75,
    market_context=context,
    memory_results=memory
)

for r in result:
    print(r)
from prediction.market_bias import MarketBiasResult
from prediction.market_regime import MarketRegimeResult
from prediction.volatility_engine import VolatilityResult

from prediction.market_context import MarketContextEngine

engine = MarketContextEngine()

bias = MarketBiasResult(

    bias="BEARISH",

    score=25.84,

    reason="Historical statistics favour downside continuation."

)

regime = MarketRegimeResult(

    regime="RANGE",

    trend_strength=50,

    volatility="NORMAL",

    suggested_style="MEAN REVERSION",

    confidence=50

)

volatility = VolatilityResult(

    atr=262.28,

    atr_percent=1.10,

    volatility_level="NORMAL",

    position_size_factor=0.75,

    suggested_action="NORMAL POSITION"

)

result = engine.run(

    bias,

    regime,

    volatility

)

print(result)
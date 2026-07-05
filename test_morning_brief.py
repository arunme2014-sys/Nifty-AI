from prediction.morning_brief import MorningBriefEngine
from prediction.market_bias import MarketBiasEngine
from prediction.market_regime import MarketRegimeEngine
from prediction.volatility_engine import VolatilityEngine
from prediction.trade_planner import TradePlannerEngine
from prediction.risk_reward import RiskRewardEngine
from prediction.decision_score import DecisionScoreEngine
from prediction.explainability import ExplainabilityEngine
from prediction.support_target import SupportResistanceEngine
from prediction.price_projection import PriceProjectionEngine

import pandas as pd

current_price = 23865.75

similar_df = pd.DataFrame({
    "return_5d":[
        -1.0,-0.8,-2.1,1.2,-1.4,-0.7,-0.9,-1.8,2.0,-1.1
    ]
})

bias = MarketBiasEngine().evaluate(
    bullish_rate=20,
    bearish_rate=80,
    confidence=30.59,
    avg5=-1.04,
    avg10=1.46
)

projection = PriceProjectionEngine().project(similar_df)

sr = SupportResistanceEngine().run(
    current_price,
    [23784.95,23397.30,23070.15],
    [24189.25,24261.60,24482.10]
)

trade = TradePlannerEngine().run(
    current_price=current_price,
    bias=bias.bias,
    support=sr.support,
    resistance=sr.resistance,
    expected_move_5d=projection.expected_5d,
    confidence=projection.confidence
)

risk = RiskRewardEngine().run(
    trade_type=trade.trade_type,
    current_price=current_price,
    entry_low=trade.entry_low,
    entry_high=trade.entry_high,
    stop_loss=trade.stop_loss,
    target1=trade.target1,
    target2=trade.target2
)

regime = MarketRegimeEngine().run(
    current_price=current_price,
    ema20=23826.67,
    ema50=23848.63,
    ema200=24430.56,
    atr=262.28,
    rsi=51.69,
    macd=82.71,
    macd_signal=51.55
)

volatility = VolatilityEngine().run(
    current_price=current_price,
    atr=262.28
)

explainability = ExplainabilityEngine().run(
    bias,
    projection,
    sr,
    trade,
    risk
)

decision = DecisionScoreEngine().run(
    bias,
    regime,
    volatility,
    risk,
    explainability
)

brief = MorningBriefEngine().run(
    current_price,
    bias,
    regime,
    volatility,
    trade,
    risk,
    decision,
    explainability
)

print(brief.report)
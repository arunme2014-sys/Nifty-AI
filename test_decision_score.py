from prediction.market_bias import MarketBiasEngine
from prediction.market_regime import MarketRegimeEngine
from prediction.volatility_engine import VolatilityEngine
from prediction.risk_reward import RiskRewardEngine
from prediction.decision_score import DecisionScoreEngine

# Market Bias
bias = MarketBiasEngine().evaluate(
    bullish_rate=20,
    bearish_rate=80,
    confidence=30.59,
    avg5=-1.04,
    avg10=1.46
)

# Market Regime
regime = MarketRegimeEngine().run(
    current_price=23865.75,
    ema20=23826.67,
    ema50=23848.63,
    ema200=24430.56,
    atr=262.28,
    rsi=51.69,
    macd=82.71,
    macd_signal=51.55
)

# Volatility
volatility = VolatilityEngine().run(
    current_price=23865.75,
    atr=262.28
)

# Risk Reward
risk = RiskRewardEngine().run(
    trade_type="SELL ON RISE",
    current_price=23865.75,
    entry_low=24140.87,
    entry_high=24189.25,
    stop_loss=24310.20,
    target1=23784.95,
    target2=23627.44
)

# Final Decision
decision = DecisionScoreEngine().run(
    bias,
    regime,
    volatility,
    risk
)

print(decision)
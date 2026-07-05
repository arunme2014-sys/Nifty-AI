from prediction.market_bias import MarketBiasEngine
from prediction.price_projection import PriceProjectionEngine
from prediction.support_target import SupportResistanceEngine
from prediction.trade_planner import TradePlannerEngine
from prediction.risk_reward import RiskRewardEngine
from prediction.report_generator import ReportGenerator

import pandas as pd

# --------------------------------------
# Sample Data
# --------------------------------------

current_price = 23865.75

# Package 1

bias_engine = MarketBiasEngine()

bias = bias_engine.evaluate(
    bullish_rate=20,
    bearish_rate=80,
    confidence=30.59,
    avg5=-1.04,
    avg10=1.46
)

# Package 2

projection_engine = PriceProjectionEngine()

similar_df = pd.DataFrame({

    "return_5d":[
        -1.0,
        -0.8,
        -2.1,
        1.2,
        -1.4,
        -0.7,
        -0.9,
        -1.8,
        2.0,
        -1.1
    ]

})

projection = projection_engine.project(similar_df)

# Package 3

sr_engine = SupportResistanceEngine()

sr = sr_engine.run(

    current_price,

    supports=[
        23784.95,
        23397.30,
        23070.15
    ],

    resistances=[
        24189.25,
        24261.60,
        24482.10
    ]

)

# Package 4

planner = TradePlannerEngine()

trade = planner.run(

    current_price=current_price,

    bias=bias.bias,

    support=sr.support,

    resistance=sr.resistance,

    expected_move_5d=projection.expected_5d,

    confidence=projection.confidence

)

# Package 5

rr_engine = RiskRewardEngine()

risk = rr_engine.run(

    trade_type=trade.trade_type,

    current_price=current_price,

    entry_low=trade.entry_low,

    entry_high=trade.entry_high,

    stop_loss=trade.stop_loss,

    target1=trade.target1,

    target2=trade.target2

)

# Package 6

report = ReportGenerator()

report.run(

    current_price=current_price,

    market_bias=bias,

    projection=projection,

    sr=sr,

    trade=trade,

    risk=risk

)
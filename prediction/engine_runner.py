"""
Sprint 10
Package 2

Engine Runner
"""

from prediction.market_bias import MarketBiasEngine
from prediction.price_projection import PriceProjectionEngine
from prediction.support_target import SupportResistanceEngine
from prediction.trade_planner import TradePlannerEngine
from prediction.risk_reward import RiskRewardEngine


class EngineRunner:

    def __init__(self):

        self.market_bias = MarketBiasEngine()

        self.price_projection = PriceProjectionEngine()

        self.support_engine = SupportResistanceEngine()

        self.trade_planner = TradePlannerEngine()

        self.risk_reward = RiskRewardEngine()

    # -------------------------------------------------------

    def run(

        self,

        current_price,

        bullish_rate,

        bearish_rate,

        confidence,

        avg5,

        avg10,

        similar_df,

        supports,

        resistances

    ):

        # ---------------------------------------
        # Package 1
        # ---------------------------------------

        bias = self.market_bias.evaluate(

            bullish_rate,

            bearish_rate,

            confidence,

            avg5,

            avg10

        )

        # ---------------------------------------
        # Package 2
        # ---------------------------------------

        projection = self.price_projection.project(

            similar_df

        )

        # ---------------------------------------
        # Package 3
        # ---------------------------------------

        sr = self.support_engine.run(

            current_price,

            supports,

            resistances

        )

        # ---------------------------------------
        # Package 4
        # ---------------------------------------

        trade = self.trade_planner.run(

            current_price=current_price,

            bias=bias.bias,

            support=sr.support,

            resistance=sr.resistance,

            expected_move_5d=projection.expected_5d,

            confidence=projection.confidence

        )

        # ---------------------------------------
        # Package 5
        # ---------------------------------------

        risk = self.risk_reward.run(

            trade_type=trade.trade_type,

            current_price=current_price,

            entry_low=trade.entry_low,

            entry_high=trade.entry_high,

            stop_loss=trade.stop_loss,

            target1=trade.target1,

            target2=trade.target2

        )

        return {

            "bias": bias,

            "projection": projection,

            "support": sr,

            "trade": trade,

            "risk": risk

        }
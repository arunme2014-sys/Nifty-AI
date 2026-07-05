"""
Sprint 12
Package 2

Production Predictor
Part 1
"""

import pandas as pd

from prediction.data_provider import DataProvider
from prediction.engine_runner import EngineRunner
from prediction.report_generator import ReportGenerator

from prediction.explainability import ExplainabilityEngine

from prediction.market_regime import MarketRegimeEngine
from prediction.volatility_engine import VolatilityEngine
from prediction.decision_score import DecisionScoreEngine
from prediction.morning_brief import MorningBriefEngine
from validation.production_validator import ProductionValidator


class ProductionPredictor:

    def __init__(self):

        self.provider = DataProvider()

        self.runner = EngineRunner()

        self.report = ReportGenerator()

        self.explainer = ExplainabilityEngine()

        self.regime_engine = MarketRegimeEngine()

        self.volatility_engine = VolatilityEngine()

        self.decision_engine = DecisionScoreEngine()

        self.morning_brief = MorningBriefEngine()
	
        self.validator = ProductionValidator()

    # -----------------------------------------------------

    def run(self):

        print("=" * 70)
        print("NIFTY AI PRO")
        print("Production Prediction Engine")
        print("=" * 70)

        # -------------------------------------------------
        # Database Check
        # -------------------------------------------------

        if not self.provider.health_check():

            print("Database connection failed.")

            return

        # -------------------------------------------------
        # Load Latest Indicator
        # -------------------------------------------------

        indicator = self.provider.load_latest_indicator().iloc[0]

        feature = self.provider.load_latest_feature().iloc[0]

        current_price = float(indicator["close"])

        # -------------------------------------------------
        # Temporary values
        # Package 3 will replace these
        # -------------------------------------------------

        bullish_rate = 20

        bearish_rate = 80

        confidence = 30.59

        avg5 = -1.04

        avg10 = 1.46

        similar_df = pd.DataFrame({

            "return_5d": [

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

        supports = self.provider.load_supports()["low"].tolist()

        resistances = self.provider.load_resistances()["high"].tolist()

        # -------------------------------------------------
        # Main Prediction Pipeline
        # -------------------------------------------------

        result = self.runner.run(

            current_price=current_price,

            bullish_rate=bullish_rate,

            bearish_rate=bearish_rate,

            confidence=confidence,

            avg5=avg5,

            avg10=avg10,

            similar_df=similar_df,

            supports=supports,

            resistances=resistances

        )
        # -------------------------------------------------
        # Market Regime
        # -------------------------------------------------

        regime = self.regime_engine.run(

            current_price=current_price,

            ema20=indicator["ema20"],

            ema50=indicator["ema50"],

            ema200=indicator["ema200"],

            atr=indicator["atr14"],

            rsi=indicator["rsi14"],

            macd=indicator["macd"],

            macd_signal=indicator["macd_signal"]

        )

        # -------------------------------------------------
        # Volatility
        # -------------------------------------------------

        volatility = self.volatility_engine.run(

            current_price=current_price,

            atr=indicator["atr14"]

        )

        # -------------------------------------------------
        # Explainability
        # -------------------------------------------------

        explanation = self.explainer.run(

            result["bias"],

            result["projection"],

            result["support"],

            result["trade"],

            result["risk"]

        )

        # -------------------------------------------------
        # Decision Score
        # -------------------------------------------------

        decision = self.decision_engine.run(

            result["bias"],

            regime,

            volatility,

            result["risk"],

            explanation

        )

        # -------------------------------------------------
        # Morning Brief
        # -------------------------------------------------

        brief = self.morning_brief.run(

            current_price,

            result["bias"],

            regime,

            volatility,

            result["trade"],

            result["risk"],

            decision,

            explanation

        )

        print()

        print(brief.report)

        # -------------------------------------------------
        # Detailed Prediction Report
        # -------------------------------------------------

        self.report.run(

            current_price=current_price,

            market_bias=result["bias"],

            projection=result["projection"],

            sr=result["support"],

            trade=result["trade"],

            risk=result["risk"]

        )

        validation = self.validator.validate(

            current_price=current_price,

            support=result["support"].support,

            resistance=result["support"].resistance,

            risk=result["risk"].risk_points,

            reward=result["risk"].reward_points_t1,

            rr=result["risk"].risk_reward_t1,

            trade_grade=result["risk"].trade_grade,

            database_ok=self.provider.health_check()

        )

        self.validator.print_report(validation)
        # -------------------------------------------------
        # AI Explainability
        # -------------------------------------------------

        print()

        print("=" * 70)

        print("AI EXPLAINABILITY")

        print("=" * 70)

        print()

        print(f"Overall Score : {explanation.overall_score}/100")

        print()

        print("Positive Factors")

        for item in explanation.positives:

            print("✓", item)

        print()

        print("Negative Factors")

        for item in explanation.negatives:

            print("-", item)

        print()

        print("=" * 70)

        print("PRODUCTION PREDICTOR COMPLETED")

        print("=" * 70)


def main():

    predictor = ProductionPredictor()

    predictor.run()


if __name__ == "__main__":

    main()
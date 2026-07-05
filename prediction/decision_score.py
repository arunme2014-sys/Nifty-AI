"""
Sprint 11
Package 3

Decision Score Engine
Version 2
"""

from dataclasses import dataclass


@dataclass
class DecisionScoreResult:

    recommendation: str

    confidence: float

    action: str

    score: float


class DecisionScoreEngine:

    def run(

        self,

        bias,

        regime,

        volatility,

        risk,

        explainability=None

    ):

        # --------------------------------------------------
        # Direction comes ONLY from Market Bias
        # --------------------------------------------------

        if bias.bias == "BULLISH":

            recommendation = "BUY"

            score = 50

        else:

            recommendation = "SELL"

            score = 50

        # --------------------------------------------------
        # Risk Reward Adjustment
        # --------------------------------------------------

        if risk.trade_grade == "A":

            score += 20

        elif risk.trade_grade == "B":

            score += 10

        elif risk.trade_grade == "C":

            score += 5

        else:

            score -= 15

        # --------------------------------------------------
        # Market Regime Adjustment
        # --------------------------------------------------

        if recommendation == "BUY":

            if regime.regime in ("UPTREND", "STRONG UPTREND"):

                score += 15

            elif regime.regime == "RANGE":

                score -= 5

            else:

                score -= 15

        else:

            if regime.regime in ("DOWNTREND", "STRONG DOWNTREND"):

                score += 15

            elif regime.regime == "RANGE":

                score += 5

            else:

                score -= 15

        # --------------------------------------------------
        # Volatility Adjustment
        # --------------------------------------------------

        if volatility.volatility_level == "LOW":

            score += 5

        elif volatility.volatility_level == "HIGH":

            score -= 5

        elif volatility.volatility_level == "EXTREME":

            score -= 15

        # --------------------------------------------------
        # Explainability Adjustment (future ready)
        # --------------------------------------------------

        if explainability is not None:

            score += (explainability.overall_score - 50) / 5

        # --------------------------------------------------

        score = max(0, min(score, 100))

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        if score >= 85:

            confidence = "VERY HIGH"

        elif score >= 70:

            confidence = "HIGH"

        elif score >= 55:

            confidence = "MEDIUM"

        else:

            confidence = "LOW"

        # --------------------------------------------------
        # Action
        # --------------------------------------------------

        if recommendation == "BUY":

            action = "BUY ON DIP"

        else:

            action = "SELL ON RISE"

        return DecisionScoreResult(

            recommendation=recommendation,

            confidence=confidence,

            action=action,

            score=round(score,2)

        )
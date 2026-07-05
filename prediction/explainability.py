"""
Sprint 10
Package 4

AI Explainability Engine
"""

from dataclasses import dataclass


@dataclass
class ExplainabilityResult:

    overall_score: float

    reasons: list

    positives: list

    negatives: list


class ExplainabilityEngine:

    def run(

        self,

        bias,

        projection,

        sr,

        trade,

        risk

    ):

        score = 0

        positives = []

        negatives = []

        # ------------------------------------

        if bias.bias == "BULLISH":

            score += 20
            positives.append("Historical bias is Bullish")

        elif bias.bias == "BEARISH":

            score += 20
            positives.append("Historical bias is Bearish")

        # ------------------------------------

        if abs(projection.expected_5d) > 1:

            score += 20
            positives.append(
                "Historical move is statistically significant"
            )

        else:

            negatives.append(
                "Expected move is relatively small"
            )

        # ------------------------------------

        if risk.trade_grade == "A":

            score += 25
            positives.append(
                "Excellent Risk / Reward ratio"
            )

        elif risk.trade_grade == "B":

            score += 15
            positives.append(
                "Good Risk / Reward ratio"
            )

        else:

            negatives.append(
                "Weak Risk / Reward ratio"
            )

        # ------------------------------------

        if sr.risk_zone == "LOW":

            score += 15
            positives.append(
                "Price has sufficient room to move"
            )

        elif sr.risk_zone == "HIGH":

            negatives.append(
                "Price is close to a key support/resistance level"
            )

        # ------------------------------------

        if trade.trade_quality == "EXCELLENT":

            score += 20
            positives.append(
                "Trade setup quality is excellent"
            )

        elif trade.trade_quality == "WEAK":

            negatives.append(
                "Trade setup quality is weak"
            )

        score = min(score, 100)

        reasons = positives + negatives

        return ExplainabilityResult(

            overall_score=score,

            reasons=reasons,

            positives=positives,

            negatives=negatives

        )
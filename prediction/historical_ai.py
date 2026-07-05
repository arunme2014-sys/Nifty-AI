"""
NIFTY AI PRO

Historical AI Engine V2

Score Based Decision Engine
"""

from dataclasses import dataclass


@dataclass
class HistoricalAIResult:

    bullish_rate: float
    bearish_rate: float
    confidence: float

    avg1: float
    avg5: float
    avg10: float

    volatility: float

    market_regime: str

    recommendation: str


class HistoricalAIEngine:

    def evaluate(self, statistics):

        bullish = statistics.bullish_rate
        bearish = statistics.bearish_rate

        avg1 = statistics.avg1
        avg5 = statistics.avg5
        avg10 = statistics.avg10

        volatility = statistics.volatility

        # -------------------------------------------------
        # AI SCORE
        # -------------------------------------------------

        score = 50

        # Probability
        score += (bullish - bearish) * 0.60

        # Historical Returns
        score += avg1 * 3.0
        score += avg5 * 1.5
        score += avg10 * 1.0

        # Volatility Adjustment
        if volatility < 1:
            score += 8

        elif volatility < 2:
            score += 3

        else:
            score -= 8

        # Clamp
        score = max(0, min(100, score))

        confidence = round(score, 2)

        # -------------------------------------------------
        # Market Regime
        # -------------------------------------------------

        if volatility >= 2:

            regime = "HIGH VOLATILITY"

        elif volatility >= 1:

            regime = "NORMAL"

        else:

            regime = "LOW VOLATILITY"

        # -------------------------------------------------
        # Decision
        # -------------------------------------------------

        if score >= 65:

            recommendation = "BUY"

        elif score <= 35:

            recommendation = "SELL"

        else:

            recommendation = "WAIT"

        return HistoricalAIResult(

            bullish_rate=bullish,

            bearish_rate=bearish,

            confidence=confidence,

            avg1=avg1,

            avg5=avg5,

            avg10=avg10,

            volatility=volatility,

            market_regime=regime,

            recommendation=recommendation

        )


if __name__ == "__main__":

    print("Historical AI Engine V2 Ready")
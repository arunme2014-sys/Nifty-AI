"""
Sprint 9 - Package 1

Market Bias Engine

Version 2
"""

from dataclasses import dataclass


@dataclass
class MarketBiasResult:

    bias: str

    score: float

    reason: str


class MarketBiasEngine:

    def evaluate(

        self,

        bullish_rate,

        bearish_rate,

        confidence,

        avg5,

        avg10

    ):

        # -------------------------------------------------
        # Historical Edge
        # -------------------------------------------------

        edge = bullish_rate - bearish_rate

        score = 50.0

        # -----------------------------------------------
        # Historical Direction
        # -----------------------------------------------

        score += edge * 0.80

        # -----------------------------------------------
        # Historical Returns
        # -----------------------------------------------

        score += avg5 * 3.0

        score += avg10 * 2.0

        # -----------------------------------------------
        # Confidence
        # -----------------------------------------------

        score += (confidence - 50) * 0.50

        # -----------------------------------------------
        # Clamp Score
        # -----------------------------------------------

        score = max(

            0,

            min(

                100,

                score

            )

        )

        # -----------------------------------------------
        # Market Bias
        # -----------------------------------------------

        if score >= 60:

            bias = "BULLISH"

        elif score <= 40:

            bias = "BEARISH"

        else:

            bias = "SIDEWAYS"

        # -----------------------------------------------
        # Reason
        # -----------------------------------------------

        if bias == "BULLISH":

            reason = (

                "Historical edge and positive returns "

                "support bullish continuation."

            )

        elif bias == "BEARISH":

            reason = (

                "Historical edge and negative returns "

                "support bearish continuation."

            )

        else:

            reason = (

                "Historical statistics indicate "

                "a neutral market."

            )

        return MarketBiasResult(

            bias=bias,

            score=round(

                score,

                2

            ),

            reason=reason

        )


if __name__ == "__main__":

    engine = MarketBiasEngine()

    result = engine.evaluate(

        bullish_rate=60,

        bearish_rate=40,

        confidence=65,

        avg5=1.5,

        avg10=2.2

    )

    print(result)
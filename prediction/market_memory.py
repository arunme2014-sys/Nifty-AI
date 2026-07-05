"""
Sprint 13

Package 4

Market Memory Engine

Measures how often historical candles respected
a particular price level.
"""

from dataclasses import dataclass


@dataclass
class MarketMemoryResult:

    level: float
    touches: int
    score: float
    strength: str


class MarketMemoryEngine:

    def __init__(self, buffer_points=20):

        self.buffer = buffer_points

    # -----------------------------------------

    def calculate(

        self,

        level,

        candle_lows

    ):

        touches = 0

        for low in candle_lows:

            if abs(low - level) <= self.buffer:

                touches += 1

        # -----------------------------
        # Score
        # -----------------------------

        score = min(

            touches * 10,

            100

        )

        # -----------------------------
        # Strength
        # -----------------------------

        if score >= 80:

            strength = "VERY STRONG"

        elif score >= 60:

            strength = "STRONG"

        elif score >= 40:

            strength = "MODERATE"

        elif score >= 20:

            strength = "WEAK"

        else:

            strength = "VERY WEAK"

        return MarketMemoryResult(

            level=level,

            touches=touches,

            score=score,

            strength=strength

        )
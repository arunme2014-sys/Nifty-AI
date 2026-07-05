"""
Sprint 11
Package 2

Volatility Engine
"""

from dataclasses import dataclass


@dataclass
class VolatilityResult:

    atr: float

    atr_percent: float

    volatility_level: str

    position_size_factor: float

    suggested_action: str


class VolatilityEngine:

    def run(

        self,

        current_price,

        atr

    ):

        atr_percent = (atr / current_price) * 100

        # ---------------------------------

        if atr_percent < 0.80:

            level = "LOW"

            factor = 1.00

            action = "FULL POSITION"

        elif atr_percent < 1.50:

            level = "NORMAL"

            factor = 0.75

            action = "NORMAL POSITION"

        elif atr_percent < 2.50:

            level = "HIGH"

            factor = 0.50

            action = "REDUCE POSITION SIZE"

        else:

            level = "EXTREME"

            factor = 0.25

            action = "TRADE VERY LIGHT"

        return VolatilityResult(

            atr=round(atr,2),

            atr_percent=round(atr_percent,2),

            volatility_level=level,

            position_size_factor=factor,

            suggested_action=action

        )
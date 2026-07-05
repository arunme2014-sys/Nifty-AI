"""
Sprint 9 - Package 4
Trade Planner Engine
"""

from dataclasses import dataclass


@dataclass
class TradePlan:

    trade_type: str

    entry_low: float
    entry_high: float

    stop_loss: float

    target1: float
    target2: float

    trade_quality: str


class TradePlannerEngine:

    def run(

        self,

        current_price,

        bias,

        support,

        resistance,

        expected_move_5d,

        confidence

    ):

        # ------------------------------------
        # BULLISH PLAN
        # ------------------------------------

        if bias == "BULLISH":

            trade = "BUY ON DIP"

            entry_low = support

            entry_high = support * 1.002

            stop = support * 0.995

            target1 = resistance

            target2 = resistance + abs(expected_move_5d) / 100 * current_price

        # ------------------------------------
        # BEARISH PLAN
        # ------------------------------------

        elif bias == "BEARISH":

            trade = "SELL ON RISE"

            entry_low = resistance * 0.998

            entry_high = resistance

            stop = resistance * 1.005

            target1 = support

            target2 = support - abs(expected_move_5d) / 100 * current_price

        # ------------------------------------
        # SIDEWAYS
        # ------------------------------------

        else:

            trade = "NO TRADE"

            entry_low = current_price

            entry_high = current_price

            stop = current_price

            target1 = current_price

            target2 = current_price

        # ------------------------------------
        # Trade Quality
        # ------------------------------------

        if confidence >= 80:

            quality = "EXCELLENT"

        elif confidence >= 65:

            quality = "GOOD"

        elif confidence >= 50:

            quality = "AVERAGE"

        else:

            quality = "WEAK"

        return TradePlan(

            trade_type=trade,

            entry_low=round(entry_low, 2),

            entry_high=round(entry_high, 2),

            stop_loss=round(stop, 2),

            target1=round(target1, 2),

            target2=round(target2, 2),

            trade_quality=quality

        )
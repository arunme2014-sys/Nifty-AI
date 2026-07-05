"""
Sprint 9 - Package 5
Risk Reward Engine
"""

from dataclasses import dataclass


@dataclass
class RiskRewardResult:

    risk_points: float

    reward_points_t1: float
    reward_points_t2: float

    risk_reward_t1: float
    risk_reward_t2: float

    trade_grade: str

    position_size: str

    verdict: str


class RiskRewardEngine:

    def run(

        self,

        trade_type,

        current_price,

        entry_low,

        entry_high,

        stop_loss,

        target1,

        target2

    ):

        # ----------------------------
        # Average Entry
        # ----------------------------

        entry = (entry_low + entry_high) / 2

        # ----------------------------
        # BUY
        # ----------------------------

        if trade_type == "BUY ON DIP":

            risk = entry - stop_loss

            reward1 = target1 - entry

            reward2 = target2 - entry

        # ----------------------------
        # SELL
        # ----------------------------

        elif trade_type == "SELL ON RISE":

            risk = stop_loss - entry

            reward1 = entry - target1

            reward2 = entry - target2

        else:

            risk = 0

            reward1 = 0

            reward2 = 0

        # ----------------------------
        # Avoid divide by zero
        # ----------------------------

        if risk <= 0:

            rr1 = 0

            rr2 = 0

        else:

            rr1 = reward1 / risk

            rr2 = reward2 / risk

        # ----------------------------
        # Trade Grade
        # ----------------------------

        best_rr = max(rr1, rr2)

        if best_rr >= 3:

            grade = "A"

            position = "FULL"

            verdict = "STRONG TRADE"

        elif best_rr >= 2:

            grade = "B"

            position = "NORMAL"

            verdict = "GOOD TRADE"

        elif best_rr >= 1.5:

            grade = "C"

            position = "HALF"

            verdict = "AVERAGE"

        else:

            grade = "D"

            position = "SMALL"

            verdict = "AVOID"

        return RiskRewardResult(

            risk_points=round(risk, 2),

            reward_points_t1=round(reward1, 2),

            reward_points_t2=round(reward2, 2),

            risk_reward_t1=round(rr1, 2),

            risk_reward_t2=round(rr2, 2),

            trade_grade=grade,

            position_size=position,

            verdict=verdict

        )
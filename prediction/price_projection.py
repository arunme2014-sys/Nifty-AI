"""
Sprint 9 - Package 2
Price Projection Engine
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class PriceProjectionResult:
    expected_1d: float
    expected_3d: float
    expected_5d: float
    direction: str
    confidence: float


class PriceProjectionEngine:

    def project(self, similar_df: pd.DataFrame):

        if similar_df.empty:
            return PriceProjectionResult(
                0.0,
                0.0,
                0.0,
                "UNKNOWN",
                0.0
            )

        # ---------- 1 Day ----------

        if "return_1d" in similar_df.columns:
            move1 = similar_df["return_1d"].dropna().mean()
        else:
            move1 = similar_df["return_5d"].dropna().mean() / 5

        # ---------- 3 Day ----------

        move3 = move1 * 3

        # ---------- 5 Day ----------

        move5 = similar_df["return_5d"].dropna().mean()

        # ---------- Direction ----------

        if move5 > 0.30:
            direction = "BULLISH"

        elif move5 < -0.30:
            direction = "BEARISH"

        else:
            direction = "SIDEWAYS"

        # ---------- Confidence ----------

        positive = (similar_df["return_5d"] > 0).sum()
        total = len(similar_df)

        confidence = positive / total * 100

        if direction == "BEARISH":
            confidence = 100 - confidence

        return PriceProjectionResult(
            expected_1d=round(move1, 2),
            expected_3d=round(move3, 2),
            expected_5d=round(move5, 2),
            direction=direction,
            confidence=round(confidence, 2)
        )
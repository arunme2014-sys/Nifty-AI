"""
Sprint 16
Historical Statistics Engine
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class HistoricalStatisticsResult:

    bullish_rate: float
    bearish_rate: float
    confidence: float

    avg1: float
    avg5: float
    avg10: float

    volatility: float

    similar_df: pd.DataFrame


class HistoricalStatisticsEngine:

    def calculate(self, lookback_df: pd.DataFrame):

        df = lookback_df.copy()

        if df.empty:

            return HistoricalStatisticsResult(

                bullish_rate=50.0,
                bearish_rate=50.0,
                confidence=50.0,

                avg1=0.0,
                avg5=0.0,
                avg10=0.0,

                volatility=0.0,

                similar_df=pd.DataFrame()

            )

        # ----------------------------------------------------
        # Clean Data
        # ----------------------------------------------------

        df["daily_return"] = df["daily_return"].fillna(0)

        if "return_5d" not in df.columns:
            df["return_5d"] = 0

        if "return_10d" not in df.columns:
            df["return_10d"] = 0

        # ----------------------------------------------------
        # Bullish / Bearish Probability
        # ----------------------------------------------------

        bullish = (df["daily_return"] > 0).sum()

        bearish = (df["daily_return"] <= 0).sum()

        total = bullish + bearish

        if total == 0:

            bullish_rate = 50.0
            bearish_rate = 50.0

        else:

            bullish_rate = round(

                bullish * 100 / total,

                2

            )

            bearish_rate = round(

                bearish * 100 / total,

                2

            )

        # ----------------------------------------------------
        # Historical Returns
        # ----------------------------------------------------

        avg1 = round(

            df["daily_return"].mean(),

            2

        )

        avg5 = round(

            df["return_5d"].fillna(0).mean(),

            2

        )

        avg10 = round(

            df["return_10d"].fillna(0).mean(),

            2

        )

        # ----------------------------------------------------
        # Historical Volatility
        # ----------------------------------------------------

        volatility = round(

            df["daily_return"].std(),

            2

        )

        if pd.isna(volatility):

            volatility = 0.0

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = round(

            max(

                bullish_rate,

                bearish_rate

            ),

            2

        )

        # ----------------------------------------------------
        # Similar Historical Sample
        # ----------------------------------------------------

        similar_df = pd.DataFrame()

        similar_df["daily_return"] = df["daily_return"]

        similar_df["return_5d"] = df["return_5d"]

        similar_df["return_10d"] = df["return_10d"]

        return HistoricalStatisticsResult(

            bullish_rate=bullish_rate,
            bearish_rate=bearish_rate,
            confidence=confidence,

            avg1=avg1,
            avg5=avg5,
            avg10=avg10,

            volatility=volatility,

            similar_df=similar_df

        )


if __name__ == "__main__":

    print("Historical Statistics Engine Ready")
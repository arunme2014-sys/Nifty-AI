"""
Sprint 14
Package 2

Walk Forward Backtest Engine
Part 1/2
"""

from datetime import datetime
import pandas as pd

from prediction.data_provider import DataProvider
from prediction.engine_runner import EngineRunner
from prediction.historical_statistics import HistoricalStatisticsEngine
from prediction.historical_ai import HistoricalAIEngine

from backtest.models import (
    BacktestTrade,
    BacktestSummary
)


class BacktestEngine:

    def __init__(self):

        self.provider = DataProvider()

        self.runner = EngineRunner()

        self.statistics = HistoricalStatisticsEngine()

        self.historical_ai = HistoricalAIEngine()

        self.summary = BacktestSummary()

        self.trades = []

    # ---------------------------------------------------------

    def load_history(self):

        query = """
        SELECT
            candle_time,
            close
        FROM candle
        ORDER BY candle_time
        """

        return pd.read_sql(
            query,
            self.provider.engine
        )

    # ---------------------------------------------------------

    def run(self):

        print("=" * 70)
        print("NIFTY AI PRO")
        print("Historical Walk Forward Backtest")
        print("=" * 70)
        print()

        history = self.load_history()

        print(f"Historical Days : {len(history)}")
        print()

        for _, row in history.iterrows():

            trade = self.process_day(

                row["candle_time"],
                float(row["close"])

            )

            if trade is not None:

                self.trades.append(trade)

        self.calculate_summary()

        return self.trades

    # ---------------------------------------------------------

    def process_day(

        self,

        candle_date,

        current_price

    ):

        indicator_df = self.provider.load_indicator_by_date(

            candle_date.strftime("%Y-%m-%d")

        )

        feature_df = self.provider.load_feature_by_date(

            candle_date.strftime("%Y-%m-%d")

        )

        if indicator_df.empty:

            return None

        if feature_df.empty:

            return None

        indicator = indicator_df.iloc[0]

        feature = feature_df.iloc[0]

    # --------------------------------------------------
    # Historical Statistics
    # --------------------------------------------------

        lookback_df = self.provider.load_features_until_date(

        candle_date.strftime("%Y-%m-%d")

      )

        statistics = self.statistics.calculate(

        lookback_df

      )

        historical_ai = self.historical_ai.evaluate(

        statistics

      )

        bullish_rate = historical_ai.bullish_rate

        bearish_rate = historical_ai.bearish_rate

        confidence = historical_ai.confidence

        avg5 = historical_ai.avg5

        avg10 = historical_ai.avg10

        similar_df = statistics.similar_df

        supports = self.provider.load_supports()["low"].tolist()

        resistances = self.provider.load_resistances()["high"].tolist()

        result = self.runner.run(

            current_price=current_price,

            bullish_rate=bullish_rate,

            bearish_rate=bearish_rate,

            confidence=confidence,

            avg5=avg5,

            avg10=avg10,

            similar_df=similar_df,

            supports=supports,

            resistances=resistances

        )

        trade = BacktestTrade(

            trade_date=candle_date,

            current_price=current_price,

            recommendation=result["trade"].trade_type,

            confidence=result["projection"].confidence,

            market_context="UNKNOWN",

            trade_grade=result["risk"].trade_grade,

            entry=result["trade"].entry_low,

            stop_loss=result["trade"].stop_loss,

            target1=result["trade"].target1,

            target2=result["trade"].target2

        )

        return trade
    # ---------------------------------------------------------

    def calculate_summary(self):

        self.summary.total_trades = len(self.trades)

        for trade in self.trades:

            recommendation = trade.recommendation.upper()

            if "BUY" in recommendation:

                self.summary.buy_trades += 1

            elif "SELL" in recommendation:

                self.summary.sell_trades += 1

            else:

                self.summary.wait_trades += 1

        return self.summary

    # ---------------------------------------------------------

    def print_summary(self):

        print()

        print("=" * 70)
        print("BACKTEST SUMMARY")
        print("=" * 70)

        print()

        print(f"Total Trades : {self.summary.total_trades}")

        print(f"BUY Trades   : {self.summary.buy_trades}")

        print(f"SELL Trades  : {self.summary.sell_trades}")

        print(f"WAIT Trades  : {self.summary.wait_trades}")

        print()

        print("=" * 70)

    # ---------------------------------------------------------

    def export_csv(

        self,

        filename="backtest/results/walk_forward.csv"

    ):

        rows = []

        for trade in self.trades:

            rows.append({

                "Date": trade.trade_date,

                "Price": trade.current_price,

                "Recommendation": trade.recommendation,

                "Confidence": trade.confidence,

                "MarketContext": trade.market_context,

                "TradeGrade": trade.trade_grade,

                "Entry": trade.entry,

                "StopLoss": trade.stop_loss,

                "Target1": trade.target1,

                "Target2": trade.target2,

                "Result": trade.result,

                "ExitPrice": trade.exit_price,

                "PnL": trade.pnl_points,

                "RiskReward": trade.risk_reward,

                "HoldingDays": trade.holding_days

            })

        df = pd.DataFrame(rows)

        df.to_csv(

            filename,

            index=False

        )

        print()

        print(f"Results exported : {filename}")

        return df


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    engine = BacktestEngine()

    engine.run()

    engine.print_summary()

    engine.export_csv()


if __name__ == "__main__":

    main()
"""
NIFTY AI PRO
Sprint 15

Trade Simulator
"""

from dataclasses import dataclass

import pandas as pd

from prediction.data_provider import DataProvider

from backtest.models import (
    BacktestTrade,
    WalkForwardResult
)


class TradeSimulator:

    def __init__(self):

        self.provider = DataProvider()

    # ---------------------------------------------------------

    def load_future_candles(

        self,

        candle_date,

        lookahead=5

    ):

        query = f"""
        SELECT

            candle_time,
            open,
            high,
            low,
            close

        FROM candle

        WHERE candle_time > '{candle_date}'

        ORDER BY candle_time

        LIMIT {lookahead}
        """

        return pd.read_sql(

            query,

            self.provider.engine

        )

    # ---------------------------------------------------------

    def simulate(

        self,

        trade: BacktestTrade

    ) -> WalkForwardResult:

        candles = self.load_future_candles(

            trade.trade_date

        )

        if candles.empty:

            return WalkForwardResult(

                trade=trade

            )

        recommendation = trade.recommendation.upper()

        if "BUY" in recommendation:

            self._simulate_buy(

                trade,

                candles

            )

        elif "SELL" in recommendation:

            self._simulate_sell(

                trade,

                candles

            )

        return WalkForwardResult(

            trade=trade

        )

    # ---------------------------------------------------------

    def _simulate_buy(

        self,

        trade,

        candles

    ):

        for index, candle in candles.iterrows():

            trade.holding_days += 1

            low = float(

                candle["low"]

            )

            high = float(

                candle["high"]

            )

            if low <= trade.stop_loss:

                trade.result = "LOSS"

                trade.exit_price = trade.stop_loss

                trade.pnl_points = round(

                    trade.stop_loss -

                    trade.entry,

                    2

                )

                return

            if high >= trade.target2:

                trade.result = "TARGET2"

                trade.exit_price = trade.target2

                trade.pnl_points = round(

                    trade.target2 -

                    trade.entry,

                    2

                )

                return

            if high >= trade.target1:

                trade.result = "TARGET1"

                trade.exit_price = trade.target1

                trade.pnl_points = round(

                    trade.target1 -

                    trade.entry,

                    2

                )

                return
    # ---------------------------------------------------------

    def _simulate_sell(

        self,

        trade,

        candles

    ):

        for _, candle in candles.iterrows():

            trade.holding_days += 1

            low = float(candle["low"])

            high = float(candle["high"])

            if high >= trade.stop_loss:

                trade.result = "LOSS"

                trade.exit_price = trade.stop_loss

                trade.pnl_points = round(

                    trade.entry - trade.stop_loss,

                    2

                )

                break

            if low <= trade.target2:

                trade.result = "TARGET2"

                trade.exit_price = trade.target2

                trade.pnl_points = round(

                    trade.entry - trade.target2,

                    2

                )

                break

            if low <= trade.target1:

                trade.result = "TARGET1"

                trade.exit_price = trade.target1

                trade.pnl_points = round(

                    trade.entry - trade.target1,

                    2

                )

                break

        if trade.result == "PENDING":

            trade.result = "NO EXIT"

            trade.exit_price = float(

                candles.iloc[-1]["close"]

            )

            trade.pnl_points = round(

                trade.entry - trade.exit_price,

                2

            )

        risk = abs(

            trade.entry - trade.stop_loss

        )

        reward = abs(

            trade.pnl_points

        )

        if risk > 0:

            trade.risk_reward = round(

                reward / risk,

                2

            )
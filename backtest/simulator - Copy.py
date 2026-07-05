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
from backtest.simulator import TradeSimulator
from backtest.models import BacktestTrade
from datetime import datetime

trade = BacktestTrade(
    trade_date=datetime(2026, 6, 30),
    current_price=23865.75,
    recommendation="SELL",
    confidence="HIGH",
    market_context="RANGE",
    trade_grade="A",
    entry=23890,
    stop_loss=24060,
    target1=23820,
    target2=23660
)

simulator = TradeSimulator()

result = simulator.simulate(trade)

print(result)
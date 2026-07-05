"""
NIFTY AI PRO
Sprint 15

Backtest Performance Report
"""

import pandas as pd

from backtest.models import (
    BacktestTrade,
    BacktestSummary
)


class BacktestReport:

    def __init__(self):

        self.summary = BacktestSummary()

    # ---------------------------------------------------------

    def build_summary(

        self,

        trades

    ):

        self.summary.total_trades = len(trades)

        profits = []

        losses = []

        equity = []

        running_equity = 0

        max_equity = 0

        max_drawdown = 0

        for trade in trades:

            pnl = trade.pnl_points

            running_equity += pnl

            equity.append(running_equity)

            if running_equity > max_equity:

                max_equity = running_equity

            drawdown = max_equity - running_equity

            if drawdown > max_drawdown:

                max_drawdown = drawdown

            recommendation = trade.recommendation.upper()

            if "BUY" in recommendation:

                self.summary.buy_trades += 1

            elif "SELL" in recommendation:

                self.summary.sell_trades += 1

            else:

                self.summary.wait_trades += 1

            if pnl > 0:

                self.summary.winning_trades += 1

                profits.append(pnl)

            elif pnl < 0:

                self.summary.losing_trades += 1

                losses.append(abs(pnl))

        self.summary.max_drawdown = round(

            max_drawdown,

            2

        )

        executed_trades = (
            self.summary.winning_trades +
            self.summary.losing_trades
        )

        if executed_trades > 0:

            self.summary.win_rate = round(
                self.summary.winning_trades * 100 /
                executed_trades,
                2
            )

        else:

            self.summary.win_rate = 0

        if profits:

            self.summary.average_profit = round(
                sum(profits) / len(profits),
                2
            )

        if losses:

            self.summary.average_loss = round(
                sum(losses) / len(losses),
                2
            )

        total_profit = sum(profits)
        total_loss = sum(losses)

        if total_loss > 0:

            self.summary.profit_factor = round(
                total_profit / total_loss,
                2
            )

        total_rr = 0

        rr_count = 0

        for trade in trades:

            if trade.risk_reward > 0:

                total_rr += trade.risk_reward
                rr_count += 1

        if rr_count:

            self.summary.average_rr = round(
                total_rr / rr_count,
                2
            )

        if executed_trades > 0:

            self.summary.expectancy = round(
                running_equity / executed_trades,
                2
            )

        else:

            self.summary.expectancy = 0
        return self.summary

    # ---------------------------------------------------------

    def print_report(self):

        s = self.summary

        print()

        print("=" * 70)

        print("NIFTY AI PRO")

        print("BACKTEST PERFORMANCE REPORT")

        print("=" * 70)

        print()

        print(f"Total Trades      : {s.total_trades}")

        print(f"BUY Trades        : {s.buy_trades}")

        print(f"SELL Trades       : {s.sell_trades}")

        print(f"WAIT Trades       : {s.wait_trades}")

        print()

        print(f"Winning Trades    : {s.winning_trades}")

        print(f"Losing Trades     : {s.losing_trades}")

        print(f"Win Rate          : {s.win_rate}%")

        print()

        print(f"Average Profit    : {s.average_profit}")

        print(f"Average Loss      : {s.average_loss}")

        print(f"Average RR        : {s.average_rr}")

        print(f"Profit Factor     : {s.profit_factor}")

        print(f"Expectancy        : {s.expectancy}")

        print(f"Max Drawdown      : {s.max_drawdown}")

        print()

        print("=" * 70)

    # ---------------------------------------------------------

    def export_csv(

        self,

        filename="backtest/results/performance_report.csv"

    ):

        s = self.summary

        df = pd.DataFrame([{

            "TotalTrades": s.total_trades,

            "BuyTrades": s.buy_trades,

            "SellTrades": s.sell_trades,

            "WaitTrades": s.wait_trades,

            "WinningTrades": s.winning_trades,

            "LosingTrades": s.losing_trades,

            "WinRate": s.win_rate,

            "AverageProfit": s.average_profit,

            "AverageLoss": s.average_loss,

            "AverageRR": s.average_rr,

            "ProfitFactor": s.profit_factor,

            "Expectancy": s.expectancy,

            "MaxDrawdown": s.max_drawdown

        }])

        df.to_csv(

            filename,

            index=False

        )

        print()

        print(

            f"Performance report exported : {filename}"

        )

        return df


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    report = BacktestReport()

    report.build_summary([])

    report.print_report()
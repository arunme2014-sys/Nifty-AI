"""
NIFTY AI PRO

Production Backtest Runner

Version 1.0
"""

from backtest.engine import BacktestEngine
from backtest.simulator import TradeSimulator
from backtest.report import BacktestReport


def main():

    print("=" * 70)
    print("NIFTY AI PRO")
    print("END TO END BACKTEST")
    print("=" * 70)
    print()

    # -----------------------------------------
    # Generate Trade Ideas
    # -----------------------------------------

    engine = BacktestEngine()

    trades = engine.run()

    engine.print_summary()

    print()

    # -----------------------------------------
    # Simulate Every Trade
    # -----------------------------------------

    simulator = TradeSimulator()

    completed_trades = []

    print("Running Trade Simulator...")

    for trade in trades:

        result = simulator.simulate(trade)

        completed_trades.append(result.trade)

    print(f"Completed : {len(completed_trades)} trades")

    print()

    # -----------------------------------------
    # Build Performance Report
    # -----------------------------------------

    report = BacktestReport()

    report.build_summary(completed_trades)

    report.print_report()

    report.export_csv()

    # -----------------------------------------
    # Export Final Trade Log
    # -----------------------------------------

    engine.trades = completed_trades

    engine.export_csv(

        "backtest/results/final_backtest.csv"

    )

    print()

    print("=" * 70)

    print("BACKTEST COMPLETED")

    print("=" * 70)


if __name__ == "__main__":

    main()
"""
Sprint 9 - Package 6
Professional Report Generator
"""

from datetime import datetime


class ReportGenerator:

    def run(

        self,

        current_price,

        market_bias,

        projection,

        sr,

        trade,

        risk

    ):

        print("\n" + "=" * 70)
        print("NIFTY AI PRO")
        print("AI PREDICTION REPORT")
        print("=" * 70)

        print(f"\nAnalysis Date : {datetime.now().strftime('%Y-%m-%d')}")

        print(f"Current Price : {current_price:.2f}")

        print("\n" + "-" * 70)
        print("MARKET OUTLOOK")
        print("-" * 70)

        print(f"Market Bias        : {market_bias.bias}")
        print(f"Bias Score         : {market_bias.score:.2f}")
        print(f"Reason             : {market_bias.reason}")

        print("\nExpected Move")

        print(f"Tomorrow           : {projection.expected_1d:.2f}%")
        print(f"3 Days             : {projection.expected_3d:.2f}%")
        print(f"5 Days             : {projection.expected_5d:.2f}%")

        print("\n" + "-" * 70)
        print("SUPPORT / RESISTANCE")
        print("-" * 70)

        print(f"Nearest Support    : {sr.support:.2f}")
        print(f"Nearest Resistance : {sr.resistance:.2f}")

        print(f"Support Distance   : {sr.support_distance:.2f}%")
        print(f"Resistance Distance: {sr.resistance_distance:.2f}%")

        print(f"Risk Zone          : {sr.risk_zone}")

        print("\n" + "-" * 70)
        print("TRADE PLAN")
        print("-" * 70)

        print(f"Trade Type         : {trade.trade_type}")

        print(
            f"Entry Zone         : "
            f"{trade.entry_low:.2f} - {trade.entry_high:.2f}"
        )

        print(f"Stop Loss          : {trade.stop_loss:.2f}")

        print(f"Target 1           : {trade.target1:.2f}")
        print(f"Target 2           : {trade.target2:.2f}")

        print(f"Trade Quality      : {trade.trade_quality}")

        print("\n" + "-" * 70)
        print("RISK ANALYSIS")
        print("-" * 70)

        print(f"Risk               : {risk.risk_points:.2f} points")

        print(f"Reward (T1)        : {risk.reward_points_t1:.2f} points")
        print(f"Reward (T2)        : {risk.reward_points_t2:.2f} points")

        print(f"RR (T1)            : {risk.risk_reward_t1:.2f}")
        print(f"RR (T2)            : {risk.risk_reward_t2:.2f}")

        print(f"Trade Grade        : {risk.trade_grade}")
        print(f"Position Size      : {risk.position_size}")
        print(f"Verdict            : {risk.verdict}")

        print("\n" + "=" * 70)
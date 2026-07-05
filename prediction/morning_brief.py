"""
Sprint 11
Package 4

Morning Brief Engine
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MorningBrief:

    report: str


class MorningBriefEngine:

    def run(

        self,

        current_price,

        bias,

        regime,

        volatility,

        trade,

        risk,

        decision,

        explainability

    ):

        lines = []

        lines.append("=" * 70)
        lines.append("NIFTY AI PRO")
        lines.append("MORNING MARKET BRIEF")
        lines.append("=" * 70)

        lines.append("")
        lines.append(f"Date              : {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"Current Price     : {current_price:.2f}")

        lines.append("")
        lines.append("-" * 70)
        lines.append("MARKET OVERVIEW")
        lines.append("-" * 70)

        lines.append(f"Market Bias       : {bias.bias}")
        lines.append(f"Market Regime     : {regime.regime}")
        lines.append(f"Volatility        : {volatility.volatility_level}")

        lines.append("")
        lines.append("-" * 70)
        lines.append("AI DECISION")
        lines.append("-" * 70)

        lines.append(f"Recommendation    : {decision.recommendation}")
        lines.append(f"Confidence        : {decision.confidence}")
        lines.append(f"AI Score          : {decision.score}/100")

        lines.append("")
        lines.append("-" * 70)
        lines.append("TRADE PLAN")
        lines.append("-" * 70)

        lines.append(f"Trade             : {trade.trade_type}")

        lines.append(
            f"Entry Zone        : {trade.entry_low:.2f} - {trade.entry_high:.2f}"
        )

        lines.append(f"Stop Loss         : {trade.stop_loss:.2f}")

        lines.append(f"Target 1          : {trade.target1:.2f}")
        lines.append(f"Target 2          : {trade.target2:.2f}")

        lines.append("")
        lines.append("-" * 70)
        lines.append("RISK MANAGEMENT")
        lines.append("-" * 70)

        lines.append(f"Trade Grade       : {risk.trade_grade}")
        lines.append(f"Risk Reward T1    : {risk.risk_reward_t1:.2f}")
        lines.append(f"Risk Reward T2    : {risk.risk_reward_t2:.2f}")

        lines.append(f"Position Size     : {volatility.suggested_action}")

        lines.append("")
        lines.append("-" * 70)
        lines.append("AI SUMMARY")
        lines.append("-" * 70)

        for item in explainability.positives:
            lines.append(f"✓ {item}")

        if explainability.negatives:

            lines.append("")

            for item in explainability.negatives:
                lines.append(f"- {item}")

        lines.append("")
        lines.append("=" * 70)

        return MorningBrief(

            report="\n".join(lines)

        )
"""
Sprint 13 - Package 2

Market Context Engine
"""

from dataclasses import dataclass


@dataclass
class MarketContextResult:

    context: str
    trading_style: str
    confidence: int
    reason: str


class MarketContextEngine:

    def run(
        self,
        market_bias,
        market_regime,
        volatility
    ):

        bias = market_bias.bias.upper()

        regime = market_regime.regime.upper()

        vol = volatility.volatility_level.upper()

        # ------------------------------------

        if regime == "STRONG UPTREND":

            context = "STRONG BULL"

            style = "BUY ON DIP"

            confidence = 95

            reason = "Strong bullish trend."

        elif regime == "UPTREND":

            context = "BULL"

            style = "BUY PULLBACK"

            confidence = 85

            reason = "Bullish trend."

        elif regime == "RANGE":

            context = "RANGE"

            style = "MEAN REVERSION"

            confidence = 80

            reason = "Range market."

        elif regime == "DOWNTREND":

            context = "BEAR"

            style = "SELL ON RISE"

            confidence = 85

            reason = "Bearish trend."

        else:

            context = "STRONG BEAR"

            style = "SELL AGGRESSIVELY"

            confidence = 95

            reason = "Strong bearish trend."

        # ------------------------------------

        if vol == "HIGH":

            confidence -= 10

            style += " (REDUCE POSITION SIZE)"

            reason += " High volatility."

        elif vol == "EXTREME":

            confidence -= 20

            style += " (VERY SMALL POSITION)"

            reason += " Extreme volatility."

        elif vol == "LOW":

            confidence += 5

            reason += " Stable volatility."

        confidence = max(0, min(confidence, 100))

        return MarketContextResult(

            context=context,

            trading_style=style,

            confidence=confidence,

            reason=reason

        )
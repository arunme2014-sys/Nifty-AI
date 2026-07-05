"""
Sprint 11
Package 1

Market Regime Engine
"""

from dataclasses import dataclass


@dataclass
class MarketRegimeResult:

    regime: str

    trend_strength: float

    volatility: str

    suggested_style: str

    confidence: float


class MarketRegimeEngine:

    def run(

        self,

        current_price,

        ema20,

        ema50,

        ema200,

        atr,

        rsi,

        macd,

        macd_signal

    ):

        score = 0

        # -----------------------------------
        # Trend
        # -----------------------------------

        if current_price > ema20:
            score += 15

        if current_price > ema50:
            score += 20

        if current_price > ema200:
            score += 30

        # -----------------------------------
        # Momentum
        # -----------------------------------

        if macd > macd_signal:
            score += 15

        if rsi > 55:
            score += 10

        elif rsi < 45:
            score -= 10

        # -----------------------------------
        # ATR
        # -----------------------------------

        atr_percent = (atr / current_price) * 100

        if atr_percent < 0.8:

            volatility = "LOW"

        elif atr_percent < 1.8:

            volatility = "NORMAL"

        else:

            volatility = "HIGH"

        # -----------------------------------
        # Regime
        # -----------------------------------

        if score >= 80:

            regime = "STRONG UPTREND"

            style = "BUY ON DIP"

        elif score >= 60:

            regime = "UPTREND"

            style = "BUY PULLBACK"

        elif score >= 40:

            regime = "RANGE"

            style = "MEAN REVERSION"

        elif score >= 20:

            regime = "DOWNTREND"

            style = "SELL ON RISE"

        else:

            regime = "STRONG DOWNTREND"

            style = "SELL AGGRESSIVELY"

        return MarketRegimeResult(

            regime=regime,

            trend_strength=round(score, 2),

            volatility=volatility,

            suggested_style=style,

            confidence=min(score, 100)

        )
"""
Sprint 13 - Package 1
Institutional Support & Resistance Engine (Phase 1)
"""

from dataclasses import dataclass


@dataclass
class SupportResistanceResult:
    support: float
    resistance: float
    support_distance: float
    resistance_distance: float
    risk_zone: str


class SupportResistanceEngine:

    def __init__(self, min_distance_points=50):
        """
        Ignore swing levels that are too close to current price.
        This value can later be optimized through backtesting.
        """
        self.min_distance_points = min_distance_points

    def run(
        self,
        current_price,
        supports,
        resistances
    ):

        # -------------------------
        # Institutional Support Filter
        # -------------------------

        valid_supports = [
            s for s in supports
            if (
                s <= current_price and
                (current_price - s) >= self.min_distance_points
            )
        ]

        if valid_supports:
            selected_support = max(valid_supports)
        else:
            # Fallback to nearest support
            fallback = [s for s in supports if s <= current_price]

            if fallback:
                selected_support = max(fallback)
            else:
                selected_support = min(supports)

        # -------------------------
        # Institutional Resistance Filter
        # -------------------------

        valid_resistances = [
            r for r in resistances
            if (
                r >= current_price and
                (r - current_price) >= self.min_distance_points
            )
        ]

        if valid_resistances:
            selected_resistance = min(valid_resistances)
        else:
            # Fallback to nearest resistance
            fallback = [r for r in resistances if r >= current_price]

            if fallback:
                selected_resistance = min(fallback)
            else:
                selected_resistance = max(resistances)

        # -------------------------
        # Distance
        # -------------------------

        support_distance = (
            (current_price - selected_support)
            / current_price
        ) * 100

        resistance_distance = (
            (selected_resistance - current_price)
            / current_price
        ) * 100

        nearest_level = min(
            support_distance,
            resistance_distance
        )

        if nearest_level < 0.50:
            risk = "HIGH"
        elif nearest_level < 1.50:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return SupportResistanceResult(
            support=round(selected_support, 2),
            resistance=round(selected_resistance, 2),
            support_distance=round(support_distance, 2),
            resistance_distance=round(resistance_distance, 2),
            risk_zone=risk
        )
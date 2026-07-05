"""
Sprint 13
Package 3

Institutional Swing Ranking Engine
"""

from dataclasses import dataclass


@dataclass
class SwingRankResult:

    level: float

    memory_score: float

    distance_score: float

    context_score: float

    score: float

class SwingRanker:

    def __init__(self):

        self.max_distance = 300.0

    # ----------------------------------------

    def _distance_score(
        self,
        current_price,
        level
    ):

        distance = abs(current_price - level)

        score = max(
            0,
            40 - (distance / self.max_distance) * 40
        )

        return score

    # ----------------------------------------

    def _context_score(
        self,
        context
    ):

        if context == "RANGE":

            return 30

        elif context in ("BULL", "BEAR"):

            return 25

        elif context in ("STRONG BULL", "STRONG BEAR"):

            return 20

        return 15

    # ----------------------------------------

    # ----------------------------------------

    def rank(

        self,

        current_price,

        market_context,

        memory_results

    ):

        ranked = []

        for memory in memory_results:

            distance_score = self._distance_score(

                current_price,

                memory.level

            )

            context_score = self._context_score(

                market_context.context

            )

            final_score = (

                memory.score

                +

                distance_score

                +

                context_score

            )

            ranked.append(

                SwingRankResult(

                    level=memory.level,

                    memory_score=memory.score,

                    distance_score=round(distance_score, 2),

                    context_score=context_score,

                    score=round(final_score, 2)

                )

            )

        ranked.sort(

            key=lambda x: x.score,

            reverse=True

        )

        return ranked
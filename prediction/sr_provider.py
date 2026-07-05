"""
Sprint 10
Package 1A

Support / Resistance Provider

Uses the Feature Store (Sprint 7) to retrieve
confirmed swing highs and swing lows instead of
raw candle highs/lows.
"""

import pandas as pd
from sqlalchemy import create_engine

from config.settings import DATABASE_URL


class SupportResistanceProvider:

    def __init__(self):

        self.engine = create_engine(DATABASE_URL)

    # --------------------------------------------------

    def load_supports(self):

        query = """

        SELECT

            c.candle_time,
            c.low

        FROM candle c

        JOIN feature_store f
            ON c.id = f.candle_id

        WHERE f.swing_low = TRUE

        ORDER BY c.candle_time DESC

        LIMIT 20

        """

        df = pd.read_sql(query, self.engine)

        return df

    # --------------------------------------------------

    def load_resistances(self):

        query = """

        SELECT

            c.candle_time,
            c.high

        FROM candle c

        JOIN feature_store f
            ON c.id = f.candle_id

        WHERE f.swing_high = TRUE

        ORDER BY c.candle_time DESC

        LIMIT 20

        """

        df = pd.read_sql(query, self.engine)

        return df

    # --------------------------------------------------

    def latest_levels(self):

        supports = self.load_supports()
        resistances = self.load_resistances()

        return {

            "supports": supports["low"].tolist(),

            "resistances": resistances["high"].tolist(),

            "support_df": supports,

            "resistance_df": resistances

        }
"""
Sprint 14
Production Data Provider

Reads live and historical market data from PostgreSQL.
Supports:
- Latest feature/indicator loading
- Historical feature/indicator loading (for backtesting)
- Swing support/resistance loading
- Recent candle loading
"""

import pandas as pd
from sqlalchemy import create_engine

from config.settings import DATABASE_URL


class DataProvider:

    def __init__(self):

        self.engine = create_engine(DATABASE_URL)

    # -------------------------------------------------
    # ALL FEATURES
    # -------------------------------------------------

    def load_features(self):

        query = """
        SELECT *
        FROM feature_store
        ORDER BY candle_id
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # LATEST FEATURE
    # -------------------------------------------------

    def load_latest_feature(self):

        query = """
        SELECT *
        FROM feature_store
        ORDER BY candle_id DESC
        LIMIT 1
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # HISTORICAL FEATURE
    # -------------------------------------------------

   
    def load_feature_by_date(self, candle_date):

        query = f"""
        SELECT
            f.*
        FROM feature_store f
        JOIN candle c
            ON c.id = f.candle_id
        WHERE DATE(c.candle_time) = '{candle_date}'
        LIMIT 1
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # HISTORICAL FEATURE WINDOW
    # -------------------------------------------------

    def load_features_until_date(self, candle_date):

        query = f"""
        SELECT

            f.*,
            c.candle_time

        FROM feature_store f

        JOIN candle c
            ON c.id = f.candle_id

        WHERE DATE(c.candle_time) <= '{candle_date}'

        ORDER BY c.candle_time
        """

        return pd.read_sql(
            query,
            self.engine
        )

    # -------------------------------------------------
    # LATEST INDICATOR
    # -------------------------------------------------

    def load_latest_indicator(self):

        query = """
        SELECT

            c.candle_time,
            c.close,

            i.ema20,
            i.ema50,
            i.ema200,

            i.rsi14,

            i.macd,
            i.macd_signal,

            i.atr14

        FROM candle c

        JOIN indicator i
            ON c.id = i.candle_id

        ORDER BY c.candle_time DESC

        LIMIT 1
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # HISTORICAL INDICATOR
    # -------------------------------------------------

    def load_indicator_by_date(self, candle_date):

        query = f"""
        SELECT

            c.candle_time,
            c.close,

            i.ema20,
            i.ema50,
            i.ema200,

            i.rsi14,

            i.macd,
            i.macd_signal,

            i.atr14

        FROM candle c

        JOIN indicator i
            ON c.id = i.candle_id

        WHERE DATE(c.candle_time) = '{candle_date}'

        LIMIT 1
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # CONFIRMED SWING SUPPORTS
    # -------------------------------------------------

    def load_supports(self, limit=250):

        query = f"""
        SELECT

            c.low

        FROM feature_store f

        JOIN candle c
            ON c.id = f.candle_id

        WHERE f.swing_low = TRUE

        ORDER BY c.candle_time DESC

        LIMIT {limit}
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # CONFIRMED SWING RESISTANCES
    # -------------------------------------------------

    def load_resistances(self, limit=250):

        query = f"""
        SELECT

            c.high

        FROM feature_store f

        JOIN candle c
            ON c.id = f.candle_id

        WHERE f.swing_high = TRUE

        ORDER BY c.candle_time DESC

        LIMIT {limit}
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # RECENT CANDLES
    # -------------------------------------------------

    def load_recent_candles(self, limit=250):

        query = f"""
        SELECT *

        FROM candle

        ORDER BY candle_time DESC

        LIMIT {limit}
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # HISTORICAL CANDLES
    # -------------------------------------------------

    def load_candles_by_date(self, candle_date, lookback=250):

        query = f"""
        SELECT *

        FROM candle

        WHERE DATE(candle_time) <= '{candle_date}'

        ORDER BY candle_time DESC

        LIMIT {lookback}
        """

        return pd.read_sql(query, self.engine)

    # -------------------------------------------------
    # DATABASE HEALTH
    # -------------------------------------------------

    def health_check(self):

        try:

            pd.read_sql("SELECT 1", self.engine)
            return True

        except Exception:

            return False
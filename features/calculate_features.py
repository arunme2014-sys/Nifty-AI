import pandas as pd
from sqlalchemy import create_engine, text

from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

# ------------------------------------
# Load Candle + Indicator Data
# ------------------------------------

query = """
SELECT
    c.id,
    c.candle_time,
    c.open,
    c.high,
    c.low,
    c.close,

    i.ema20,
    i.ema50,
    i.ema200,
    i.rsi14,
    i.macd,
    i.macd_signal

FROM candle c

JOIN indicator i
ON c.id = i.candle_id

ORDER BY c.candle_time;
"""

df = pd.read_sql(query, engine)

# ------------------------------------
# Feature Calculations
# ------------------------------------

# Gap %
df["gap_percent"] = (
    (df["open"] - df["close"].shift(1))
    / df["close"].shift(1)
) * 100

# Daily Return
df["daily_return"] = (
    (df["close"] - df["open"])
    / df["open"]
) * 100

# Future Returns (for backtesting)
df["return_5d"] = (
    (df["close"].shift(-5) - df["close"])
    / df["close"]
) * 100

df["return_10d"] = (
    (df["close"].shift(-10) - df["close"])
    / df["close"]
) * 100

# EMA Distance
df["ema20_distance"] = (
    (df["close"] - df["ema20"])
    / df["ema20"]
) * 100

df["ema50_distance"] = (
    (df["close"] - df["ema50"])
    / df["ema50"]
) * 100

df["ema200_distance"] = (
    (df["close"] - df["ema200"])
    / df["ema200"]
) * 100

# Above EMA Flags
df["above_ema20"] = df["close"] > df["ema20"]
df["above_ema50"] = df["close"] > df["ema50"]
df["above_ema200"] = df["close"] > df["ema200"]

# MACD
df["bullish_macd"] = df["macd"] > df["macd_signal"]

# RSI Zones
def rsi_zone(rsi):
    if pd.isna(rsi):
        return None
    if rsi >= 70:
        return "Overbought"
    elif rsi <= 30:
        return "Oversold"
    elif rsi >= 50:
        return "Bullish"
    else:
        return "Bearish"

df["rsi_zone"] = df["rsi14"].apply(rsi_zone)

# ------------------------------------
# Swing Detection (5-Candle Fractal)
# ------------------------------------

df["swing_high"] = False
df["swing_low"] = False

for i in range(2, len(df) - 2):

    current_high = df.loc[i, "high"]
    current_low = df.loc[i, "low"]

    prev_high1 = df.loc[i - 1, "high"]
    prev_high2 = df.loc[i - 2, "high"]

    next_high1 = df.loc[i + 1, "high"]
    next_high2 = df.loc[i + 2, "high"]

    prev_low1 = df.loc[i - 1, "low"]
    prev_low2 = df.loc[i - 2, "low"]

    next_low1 = df.loc[i + 1, "low"]
    next_low2 = df.loc[i + 2, "low"]

    # Swing High
    if (
        current_high > prev_high1
        and current_high > prev_high2
        and current_high > next_high1
        and current_high > next_high2
    ):
        df.loc[i, "swing_high"] = True

    # Swing Low
    if (
        current_low < prev_low1
        and current_low < prev_low2
        and current_low < next_low1
        and current_low < next_low2
    ):
        df.loc[i, "swing_low"] = True
# ------------------------------------
# Save to PostgreSQL
# ------------------------------------

feature_df = df[
    [
        "id",
        "gap_percent",
        "daily_return",
        "return_5d",
        "return_10d",
        "ema20_distance",
        "ema50_distance",
        "ema200_distance",
        "above_ema20",
        "above_ema50",
        "above_ema200",
        "bullish_macd",
        "rsi_zone",
        "swing_high",
        "swing_low",
    ]
].copy()

feature_df.rename(columns={"id": "candle_id"}, inplace=True)

with engine.begin() as conn:
    conn.execute(text("DELETE FROM feature_store"))

feature_df.to_sql(
    "feature_store",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000,
)

print(f"✅ {len(feature_df)} feature records inserted.")
print(feature_df.tail())
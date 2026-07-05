import pandas as pd
from sqlalchemy import create_engine
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

# -----------------------------
# Database Configuration
# -----------------------------
DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "niftyai"

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# -----------------------------
# Load Candle Data
# -----------------------------
query = """
SELECT
    id,
    candle_time,
    open,
    high,
    low,
    close
FROM candle
ORDER BY candle_time;
"""

df = pd.read_sql(query, engine)

# -----------------------------
# Calculate Indicators
# -----------------------------

df["ema20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()

df["ema50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()

df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()

df["rsi14"] = RSIIndicator(close=df["close"], window=14).rsi()

macd = MACD(close=df["close"])

df["macd"] = macd.macd()
df["macd_signal"] = macd.macd_signal()
df["macd_histogram"] = macd.macd_diff()

atr = AverageTrueRange(
    high=df["high"],
    low=df["low"],
    close=df["close"],
    window=14
)

df["atr14"] = atr.average_true_range()

from sqlalchemy import text

# Remove old indicator data
with engine.begin() as conn:
    conn.execute(text("DELETE FROM indicator"))

# Keep only required columns
indicator_df = df[
    [
        "id",
        "ema20",
        "ema50",
        "ema200",
        "rsi14",
        "macd",
        "macd_signal",
        "macd_histogram",
        "atr14",
    ]
].copy()

indicator_df.rename(columns={"id": "candle_id"}, inplace=True)

# Insert into PostgreSQL
indicator_df.to_sql(
    "indicator",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000,
)

print(f"✅ {len(indicator_df)} indicator records inserted.")
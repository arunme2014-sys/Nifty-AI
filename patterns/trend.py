import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

query = """
SELECT
    c.candle_time,
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
ORDER BY c.candle_time DESC
LIMIT 1;
"""

df = pd.read_sql(query, engine)

row = df.iloc[0]

score = 0

# Price above EMA20
if row["close"] > row["ema20"]:
    score += 20

# Price above EMA50
if row["close"] > row["ema50"]:
    score += 20

# Price above EMA200
if row["close"] > row["ema200"]:
    score += 20

# RSI
if row["rsi14"] > 50:
    score += 20

# MACD
if row["macd"] > row["macd_signal"]:
    score += 20

print("=" * 60)
print("TREND ENGINE")
print("=" * 60)
print(f"Trend Score : {score}/100")

if score >= 80:
    trend = "Strong Uptrend"
elif score >= 60:
    trend = "Uptrend"
elif score >= 40:
    trend = "Sideways"
elif score >= 20:
    trend = "Downtrend"
else:
    trend = "Strong Downtrend"

print("Trend :", trend)
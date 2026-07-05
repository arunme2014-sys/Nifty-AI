import pandas as pd
from sqlalchemy import create_engine
from scipy.signal import find_peaks

from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

query = """
SELECT
    candle_time,
    high,
    low,
    close
FROM candle
ORDER BY candle_time;
"""

df = pd.read_sql(query, engine)

# -----------------------------
# Find Swing Highs
# -----------------------------
high_peaks, _ = find_peaks(
    df["high"],
    distance=5,
    prominence=80
)
print()
print("=" * 60)
print("DOUBLE TOP DETECTION")
print("=" * 60)

swing_highs = []

for i in high_peaks:
    swing_highs.append({
        "date": df.iloc[i]["candle_time"],
        "price": df.iloc[i]["high"],
        "index": i
    })

found = False

for i in range(len(swing_highs)-1):

    p1 = swing_highs[i]
    p2 = swing_highs[i+1]

    # Must be separated
    if p2["index"] - p1["index"] < 5:
        continue

    diff = abs(p1["price"] - p2["price"])
    pct = diff / p1["price"] * 100

    if pct < 1.0:
        found = True

        print(f"\nDouble Top Found")
        print(f"Peak 1 : {p1['date'].date()}  {p1['price']:.2f}")
        print(f"Peak 2 : {p2['date'].date()}  {p2['price']:.2f}")
        print(f"Difference : {pct:.2f}%")

if not found:
    print("No Double Top detected.")
# -----------------------------
# Find Swing Lows
# -----------------------------
low_peaks, _ = find_peaks(
    -df["low"],
    distance=5,
    prominence=80
)

print("=" * 60)
print("SWING HIGHS")
print("=" * 60)

for i in high_peaks[-10:]:
    print(
        f"{df.iloc[i]['candle_time'].date()}  "
        f"High = {df.iloc[i]['high']:.2f}"
    )

print()

print("=" * 60)
print("SWING LOWS")
print("=" * 60)

for i in low_peaks[-10:]:
    print(
        f"{df.iloc[i]['candle_time'].date()}  "
        f"Low = {df.iloc[i]['low']:.2f}"
    )
import pandas as pd
from sqlalchemy import create_engine, text

# Database Configuration
DB_USER = "postgres"
DB_PASSWORD = "postgres123"   # <-- Change this
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "niftyai"

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Read CSV
df = pd.read_csv("data/nifty_daily.csv")

# Rename columns
df.rename(columns={
    "Date": "candle_time",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
}, inplace=True)

# Keep only required columns
df = df[["candle_time", "open", "high", "low", "close", "volume"]]

# Insert data
with engine.begin() as conn:

    instrument_id = conn.execute(
        text("SELECT id FROM instrument WHERE symbol='NIFTY50'")
    ).scalar()

    inserted = 0

    for _, row in df.iterrows():

        conn.execute(text("""
            INSERT INTO candle
            (instrument_id,timeframe,candle_time,open,high,low,close,volume)

            VALUES
            (:instrument_id,'1D',:candle_time,:open,:high,:low,:close,:volume)

            ON CONFLICT DO NOTHING
        """), {
            "instrument_id": instrument_id,
            "candle_time": row["candle_time"],
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"])
        })

        inserted += 1

print(f"Processed {inserted} rows")
print("Import Completed")
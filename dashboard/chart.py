import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ------------------------
# Database Configuration
# ------------------------

DB_USER = "postgres"
DB_PASSWORD = "postgres123"   # <-- Replace with your password
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "niftyai"

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ------------------------
# Load Data
# ------------------------

query = """
SELECT
    candle_time,
    open,
    high,
    low,
    close
FROM candle
ORDER BY candle_time;
"""

df = pd.read_sql(query, engine)

# ------------------------
# Create Candlestick Chart
# ------------------------

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["candle_time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"]
        )
    ]
)

fig.update_layout(
    title="NIFTY 50 - Historical Candlestick",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False
)

fig.show()
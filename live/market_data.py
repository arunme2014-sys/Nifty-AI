"""
NIFTY AI PRO
Live Market Data

Compatible with:
- Python 3.11
- fyers-apiv3==3.1.12
"""

from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from fyers_apiv3 import fyersModel

from live.config import (
    CLIENT_ID,
    SYMBOL,
    TIMEFRAME,
    HISTORY_DAYS,
)

# ---------------------------------------------------------
# Read latest access token
# ---------------------------------------------------------

TOKEN_FILE = Path(__file__).parent / "access_token.txt"

if not TOKEN_FILE.exists():
    raise FileNotFoundError(
        "access_token.txt not found. Run python -m live.auth first."
    )

ACCESS_TOKEN = TOKEN_FILE.read_text(
    encoding="utf-8"
).strip()


class MarketData:

    def __init__(self):

        print("\n" + "=" * 70)
        print("FYERS CONNECTION")
        print("=" * 70)
        print("CLIENT_ID :", CLIENT_ID)
        print("TOKEN LENGTH :", len(ACCESS_TOKEN))
        print("=" * 70)

        self.fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID,
            token=ACCESS_TOKEN,
            is_async=False,
            log_path=""
        )

        print("\nChecking Authentication...\n")

        profile = self.fyers.get_profile()

        print(profile)

        if profile.get("s") != "ok":
            raise Exception(profile)

    # ---------------------------------------------------------

    def get_history(self):

        today = datetime.now().date()
        from_date = today - timedelta(days=HISTORY_DAYS)

        request = {

            "symbol": SYMBOL,

            "resolution": TIMEFRAME,

            "date_format": "1",

            "range_from": from_date.strftime("%Y-%m-%d"),

            "range_to": today.strftime("%Y-%m-%d"),

            "cont_flag": "1"

        }

        print("\nHistory Request")
        print(request)

        response = self.fyers.history(data=request)

        print("\nHistory Response")
        print(response)

        if response.get("s") != "ok":
            raise Exception(response)

        df = pd.DataFrame(

            response["candles"],

            columns=[

                "timestamp",

                "open",

                "high",

                "low",

                "close",

                "volume"

            ]

        )

        df["datetime"] = pd.to_datetime(

            df["timestamp"],

            unit="s"

        )

        return df[
            [
                "datetime",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        ]

    # ---------------------------------------------------------

    def latest_candle(self):

        return self.get_history().iloc[-1]


# ---------------------------------------------------------

if __name__ == "__main__":

    md = MarketData()

    candle = md.latest_candle()

    print("\n" + "=" * 70)
    print("LATEST NIFTY CANDLE")
    print("=" * 70)

    print(candle)
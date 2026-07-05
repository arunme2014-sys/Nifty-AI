"""
Sprint 10
Package 3

Main Prediction Application
"""

import pandas as pd

from prediction.engine_runner import EngineRunner
from prediction.report_generator import ReportGenerator


def main():

    print("=" * 70)
    print("NIFTY AI PRO")
    print("Prediction Engine")
    print("=" * 70)

    # -------------------------------------------------
    # Temporary sample data
    # (Will be replaced by PostgreSQL in next package)
    # -------------------------------------------------

    current_price = 23865.75

    bullish_rate = 20
    bearish_rate = 80

    confidence = 30.59

    avg5 = -1.04
    avg10 = 1.46

    similar_df = pd.DataFrame({

        "return_5d":[
            -1.0,
            -0.8,
            -2.1,
            1.2,
            -1.4,
            -0.7,
            -0.9,
            -1.8,
            2.0,
            -1.1
        ]

    })

    supports = [

        23784.95,
        23397.30,
        23070.15

    ]

    resistances = [

        24189.25,
        24261.60,
        24482.10

    ]

    # -------------------------------------------------

    runner = EngineRunner()

    result = runner.run(

        current_price=current_price,

        bullish_rate=bullish_rate,

        bearish_rate=bearish_rate,

        confidence=confidence,

        avg5=avg5,

        avg10=avg10,

        similar_df=similar_df,

        supports=supports,

        resistances=resistances

    )

    report = ReportGenerator()

    report.run(

        current_price=current_price,

        market_bias=result["bias"],

        projection=result["projection"],

        sr=result["support"],

        trade=result["trade"],

        risk=result["risk"]

    )


if __name__ == "__main__":

    main()
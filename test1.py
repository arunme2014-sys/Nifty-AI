import pandas as pd

from prediction.price_projection import PriceProjectionEngine

df = pd.DataFrame({

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

engine = PriceProjectionEngine()

result = engine.project(df)

print(result)
from prediction.data_provider import DataProvider

provider = DataProvider()

print(provider.load_latest_indicator())

print(provider.load_features().tail())

print(provider.load_supports().head())

print(provider.load_resistances().head())
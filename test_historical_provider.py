from prediction.data_provider import DataProvider

provider = DataProvider()

print("=" * 60)
print("FEATURE")
print("=" * 60)

print(provider.load_feature_by_date("2026-06-30"))

print("=" * 60)
print("INDICATOR")
print("=" * 60)

print(provider.load_indicator_by_date("2026-06-30"))

print("=" * 60)
print("CANDLES")
print("=" * 60)

print(provider.load_candles_by_date("2026-06-30", 5))
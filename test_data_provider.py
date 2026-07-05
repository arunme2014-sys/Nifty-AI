from prediction.data_provider import DataProvider

provider = DataProvider()

print("=" * 60)
print("LATEST INDICATOR")
print("=" * 60)

print(provider.load_latest_indicator())

print("\n")

print("=" * 60)
print("LATEST FEATURE")
print("=" * 60)

print(provider.load_latest_feature())
from prediction.data_provider import DataProvider

provider = DataProvider()

df = provider.load_features_until_date("2026-06-30")

print("=" * 60)
print(df.tail())
print("=" * 60)
print("Rows :", len(df))
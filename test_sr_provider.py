from prediction.sr_provider import SupportResistanceProvider

provider = SupportResistanceProvider()

levels = provider.latest_levels()

print("\nLatest Supports\n")
print(levels["support_df"])

print("\nLatest Resistances\n")
print(levels["resistance_df"])

print("\nSupport List")
print(levels["supports"])

print("\nResistance List")
print(levels["resistances"])
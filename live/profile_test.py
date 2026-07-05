from fyers_apiv3 import fyersModel
from live.config import CLIENT_ID, ACCESS_TOKEN

fyers = fyersModel.FyersModel(
    client_id=CLIENT_ID,
    token=ACCESS_TOKEN,
    is_async=False,
    log_path=""
)

print(fyers.get_profile())
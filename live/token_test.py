# live/token_test.py

from live.config import ACCESS_TOKEN

print("Token starts with:")
print(ACCESS_TOKEN[:25])

print("\nContains colon:", ":" in ACCESS_TOKEN)

if ":" in ACCESS_TOKEN:
    appid, jwt = ACCESS_TOKEN.split(":", 1)
    print("APPID :", appid)
    print("JWT length :", len(jwt))
else:
    print("JWT length :", len(ACCESS_TOKEN))
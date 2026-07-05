"""
NIFTY AI PRO
Live Authentication

Compatible with:
- Python 3.11
- fyers-apiv3==3.1.12
"""

from pathlib import Path
from fyers_apiv3 import fyersModel

from live.config import (
    CLIENT_ID,
    SECRET_KEY,
    REDIRECT_URI,
)


class FyersAuth:

    def __init__(self):

        self.session = fyersModel.SessionModel(
            client_id=CLIENT_ID,
            secret_key=SECRET_KEY,
            redirect_uri=REDIRECT_URI,
            response_type="code",
            grant_type="authorization_code"
        )

    # ---------------------------------------------------------

    def login_url(self):

        return self.session.generate_authcode()

    # ---------------------------------------------------------

    def generate_token(self, auth_code):

        self.session.set_token(auth_code)

        return self.session.generate_token()

    # ---------------------------------------------------------

    def connect(self, access_token):

        return fyersModel.FyersModel(
            client_id=CLIENT_ID,
            token=access_token,
            is_async=False,
            log_path=""
        )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    auth = FyersAuth()

    print("\n" + "=" * 70)
    print("FYERS LOGIN URL")
    print("=" * 70)

    login_url = auth.login_url()

    print(login_url)

    print("\nOpen the above URL in your browser.")
    print("Login to FYERS.")
    print("Copy ONLY the auth_code.")
    print()

    auth_code = input("Enter Auth Code : ").strip()

    print("\nGenerating Access Token...\n")

    response = auth.generate_token(auth_code)

    print("=" * 70)
    print("TOKEN RESPONSE")
    print("=" * 70)
    print(response)

    if response.get("s") != "ok":

        print("\nToken generation failed.")
        exit()

    access_token = response["access_token"]

    # ---------------------------------------------------------
    # Save latest access token
    # ---------------------------------------------------------

    token_file = Path(__file__).parent / "access_token.txt"

    token_file.write_text(
        access_token,
        encoding="utf-8"
    )

    print("\nAccess Token saved successfully.")
    print(token_file)

    print("\n" + "=" * 70)
    print("PROFILE TEST")
    print("=" * 70)

    fyers = auth.connect(access_token)

    profile = fyers.get_profile()

    print(profile)

    if profile.get("s") != "ok":

        print("\nAuthentication failed.")

    else:

        print("\nAuthentication Successful.")

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
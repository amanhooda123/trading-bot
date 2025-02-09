import os
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def generate_access_token():
    # Zerodha API Key and Secret
    api_key = os.getenv("ZERODHA_API_KEY")
    api_secret = os.getenv("ZERODHA_API_SECRET")

    # Zerodha Request Token (manually obtained initially)
    request_token = os.getenv("ZERODHA_REQUEST_TOKEN")  # Update this manually for the first time

    if not request_token:
        print("Error: REQUEST_TOKEN is missing. Update the environment variables.")
        return None

    # Create KiteConnect instance
    kite = KiteConnect(api_key=api_key)

    try:
        # Exchange request token for access token
        session_data = kite.generate_session(request_token, api_secret)
        access_token = session_data["access_token"]

        print("Access Token Generated:", access_token)

        # If running locally, update the .env file
        if os.getenv("LOCAL_ENV", "false").lower() == "true":
            with open(".env", "a") as env_file:
                env_file.write(f"\nZERODHA_ACCESS_TOKEN={access_token}")

        return access_token

    except Exception as e:
        print("Error generating access token:", str(e))
        return None


if __name__ == "__main__":
    generate_access_token()

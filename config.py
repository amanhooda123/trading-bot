from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Helper function to check for missing environment variables
def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value

# Telegram API Credentials
TELEGRAM_API_ID = get_env_variable("TELEGRAM_API_ID", required=True)
TELEGRAM_API_HASH = get_env_variable("TELEGRAM_API_HASH", required=True)
TELEGRAM_PHONE_NUMBER = get_env_variable("TELEGRAM_PHONE_NUMBER", required=True)
TELEGRAM_GROUP_ID = int(get_env_variable("TELEGRAM_GROUP_ID", "-1001234567890"))  # Default fallback

# OpenAI API Key
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY", required=True)

# Zerodha API Credentials
ZERODHA_API_KEY = get_env_variable("ZERODHA_API_KEY", required=True)
ZERODHA_ACCESS_TOKEN = get_env_variable("ZERODHA_ACCESS_TOKEN")

# Ensure Zerodha Access Token is Available
if ZERODHA_ACCESS_TOKEN == "to_be_generated":
    raise ValueError("ZERODHA_ACCESS_TOKEN is missing! Run `zerodha_token_refresh.py` to generate it.")

print("✅ Config loaded successfully!")  # Debugging: Print if everything is loaded correctly

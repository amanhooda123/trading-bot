from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Telegram API Credentials
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER")
TELEGRAM_GROUP_ID = int(os.getenv("TELEGRAM_GROUP_ID", "-1001234567890"))  # Default value as fallback

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Zerodha API Credentials
ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY")
ZERODHA_ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN")

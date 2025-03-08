import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram API Credentials
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
# Set your target group ID (example: 6658679157)
TELEGRAM_GROUP_ID = int(os.getenv("TELEGRAM_GROUP_ID", "6658679157"))

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dhan API Credentials
DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
DHAN_BASE_URL = "https://api.dhan.co/v2"

# CSV file for instrument lookup
SECURITY_CSV_FILE = "api-scrip-master.csv"

# Validate required variables
required_vars = [
    TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, str(TELEGRAM_GROUP_ID),
    OPENAI_API_KEY, DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN, SECURITY_CSV_FILE
]
if any(var is None for var in required_vars):
    raise ValueError("🚨 Missing one or more required configuration values!")

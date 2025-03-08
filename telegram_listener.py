from telethon import TelegramClient, events
import logging
import asyncio
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_GROUP_ID
from trade_parser import parse_trade_signal
from trade_executor import execute_trade

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Initialize Telegram client (user session)
client = TelegramClient("user_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def start_telegram_listener():
    """Logs in as a user and listens to messages from a specific Telegram group."""
    await client.start(TELEGRAM_PHONE)
    print(f"✅ Telegram user session started. Listening for messages in group: {TELEGRAM_GROUP_ID}")

    @client.on(events.NewMessage(chats=TELEGRAM_GROUP_ID))
    async def group_message_handler(event):
        """Handles messages from the Telegram group."""
        sender = await event.get_sender()
        message_text = event.raw_text
        print(f"📩 NEW MESSAGE FROM {sender.username or sender.id}: {message_text}")

        trade_details = parse_trade_signal(message_text)

        if trade_details:
            if "security_id" not in trade_details:
                print(f"⚠️ Security ID missing for trade: {trade_details}")
                return

            print(f"✅ Parsed Trade Details: {trade_details}")
            trade_response = execute_trade(trade_details)
            print(f"🚀 Trade Execution Response: {trade_response}")
        else:
            print("⚠️ No valid trade detected in message.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_telegram_listener())

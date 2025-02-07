from telethon import TelegramClient, events
import asyncio
from config.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE_NUMBER, TELEGRAM_GROUP_ID
from core.trade_parser import extract_trade_details
from core.trade_executor import execute_trade

client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

@client.on(events.NewMessage(chats=TELEGRAM_GROUP_ID))
async def new_message_listener(event):
    """ Listen for new messages in the Telegram group. """
    message_text = event.message.message
    print(f"New message received: {message_text}")

    trade_details = await extract_trade_details(message_text)  # Extract trade details using OpenAI
    print(f"Extracted Trade Details: {trade_details}")

    execute_trade(trade_details)  # Execute the trade on Zerodha

async def main():
    await client.start(TELEGRAM_PHONE_NUMBER)
    print("Listening for Telegram messages in real-time...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

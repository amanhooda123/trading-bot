from telethon import TelegramClient, events
from trade_parser import extract_trade_details
from trade_executor import execute_trade
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE_NUMBER, TELEGRAM_GROUP_ID

client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

@client.on(events.NewMessage(chats=TELEGRAM_GROUP_ID))
async def handle_message(event):
    """Handle new messages from the Telegram group."""
    message_text = event.message.message
    print(f"New message received: {message_text}")
    
    try:
        trade_details = await extract_trade_details(message_text)  # Extract trade details
        print(f"Extracted trade details: {trade_details}")
        execute_trade(trade_details)  # Execute trade
    except Exception as e:
        print(f"Error handling message: {e}")

async def start_telegram_bot():
    """Start the Telegram bot."""
    await client.start(TELEGRAM_PHONE_NUMBER)
    print("Telegram bot started!")
    await client.run_until_disconnected()
